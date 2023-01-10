from tensorflow.python.util.nest import flatten_with_tuple_paths_up_to

# %%  라이브러리 Load
import tensorflow as tf
import numpy as np
import pandas as pd
import datetime
import os
import csv
from keras.layers import Input, Dense, LSTM, Dropout
from keras.models import Model
from keras import initializers

#from keras.utils import plot_model
from keras.callbacks import EarlyStopping


def get_dataset(file_path, data_size, train_output, **kwargs):  # CSV 구성
    dataset = tf.data.experimental.make_csv_dataset(
        file_path,
        batch_size=data_size,
        label_name=train_output,
        na_value="?",  # NA / NaN 값의 처리방식 구성
        ignore_errors=True,
        **kwargs)
    return dataset


def show_batch(dataset):
    for batch, label in dataset.take(1):
        for key, value in batch.items():
            print("{:20s}: {}".format(key, value.numpy()))


def pack(feartures, label):
    return tf.stack(list(feartures.values()), axis=-1), label


def make_model(initializer):
    Input1 = Input(1, name='Input_layer')  # 독립변수 개수
    x = Dense(16, activation='relu', name='Hidden_layer1')(Input1)
    x = Dense(32, activation='relu', name='Hidden_layer2')(x)
    x = Dense(64, activation='relu', kernel_initializer=initializer,
              name='Hidden_layer3')(x)
    x = Dense(32, activation='relu', name='Hidden_layer4')(x)
    x = Dense(16, activation='relu', kernel_initializer=initializer,
              name='Hidden_layer5')(x)
    output = Dense(1, activation='softplus', name='Output_layer')(x)  # 출력층
    model = Model(inputs=Input1, outputs=output)
    return model


def train(data_path, file_name):
    # 데이터 Laod--------------------------------------------------------------------------------
    flatten_with_tuple_paths_up_to = data_path  # input 데이터 변수
    save_path = data_path

    data = pd.read_csv(data_path+file_name)
    data_size = len(data)  # 데이터 행 개수
    train_output = "Output"  # 종속변수

    column_name = ['Output', 'Vibration']
    DEFAULTS = [0.00, 0.00]

    raw_data_train = get_dataset(data_path+file_name,
                                 data_size,
                                 train_output,
                                 select_columns=column_name,
                                 column_defaults=DEFAULTS)

    packed_dataset = raw_data_train.map(pack)
    for feartures, labels in packed_dataset.take(1):
        None

    # 학습, 검증, 평가용 데이터 분류--------------------------------------------------------------------------------
    eval_size = 100
    predict_size = 100
    train_size = data_size - eval_size - predict_size

    train_x, eval_x, predict_x = feartures[:train_size,
                                           :], feartures[train_size:train_size+eval_size, :], feartures[data_size-predict_size:, :]
    train_y, eval_y, predict_y = labels[:train_size], labels[train_size:train_size +
                                                             eval_size], labels[data_size-predict_size:]

    # 모델 입력용 데이터 구성
    data_x_array = np.array(feartures)
    data_y_array = np.array(labels).reshape(len(labels), 1)
    data_xy_array = np.concatenate((data_x_array, data_y_array), axis=1)
    dataframe = pd.DataFrame(data_xy_array, columns=column_name)

    # 모델 설계--------------------------------------------------------------------------------
    initializer = tf.keras.initializers.HeNormal()  # initializer 선정
    model = make_model(initializer)
    model.summary()

    # 모델 학습--------------------------------------------------------------------------------
    model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(
        lr=0.001), metrics=['mae', 'mape'])

    # 텐서보드 자료 저장
    log_dir = os.path.join("logs",
                           "fit",
                           datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),)
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir, histogram_freq=1)
    # tensorboard --logdir=.\logs\fit\  #텐서보드 실행

    Epochs = 50  # 1000  #학습 반복횟수
    batch_fit = 100
    verbose_fit = 2  # 학습과정 보기, 0:안보여줌, 1:자세히, 2:간략히
    early_stopping = EarlyStopping(
        monitor='val_loss', min_delta=0, patience=100, mode='auto')
    history = model.fit(train_x, train_y,
                        validation_data=(eval_x, eval_y),
                        epochs=Epochs,
                        batch_size=batch_fit,
                        verbose=verbose_fit,
                        callbacks=[early_stopping])

    model_path = data_path+'학습모델.h5'
    model.save(data_path+'학습모델.h5')

    # 모델 예측--------------------------------------------------------------------------------
    predict_output = model.predict(predict_x)
    real_predict_array = np.array(predict_y).reshape(predict_size, 1)

    predictor_error = abs(predict_output - real_predict_array)
    MAE = sum(predictor_error)/len(predictor_error)
    SMAPE = predictor_error/((abs(real_predict_array)+abs(predictor_error))/2)
    mse, mae, mape = model.evaluate(predict_x, predict_y, verbose=1)

    # 예측 결과 csv 저장--------------------------------------------------------------------------------------------
    import csv
    np.set_printoptions(suppress=True)

    with open(save_path+'예측결과.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Predicted power", "Actual power",
                        "Abs error", "MAE", "MAPE"])
        writer.writerow(["", "", "", mae, mape])
        for a in range(len(predict_output)):
            writer.writerow(
                [predict_output[a][0], real_predict_array[a][0], predictor_error[a][0]])

    df = pd.read_csv(save_path+'예측결과.csv')
    fig = df.iloc[:, :2].plot().get_figure()  # 칼럼 두개만 플롯
    fig.savefig(save_path+'예측결과plot.jpg')

    return mse, mae, mape, save_path  # modifield (model_path --> save_path)


def predict(data_path, file_name, model_path):
    # 데이터 Laod--------------------------------------------------------------------------------
    flatten_with_tuple_paths_up_to = data_path  # input 데이터 변수
    save_path = data_path

    data = pd.read_csv(data_path+file_name)
    data_size = len(data)  # 데이터 행 개수
    train_output = "Output"  # 종속변수

    column_name = ['Output', 'Vibration']
    DEFAULTS = [0.00, 0.00]

    raw_data_train = get_dataset(data_path+file_name,
                                 data_size,
                                 train_output,
                                 select_columns=column_name,
                                 column_defaults=DEFAULTS)

    packed_dataset = raw_data_train.map(pack)
    for feartures, labels in packed_dataset.take(1):
        None

    predict_x = feartures[:, :]

    predict_y = labels
    model = tf.keras.models.load_model(model_path)

    predict_data = model.predict(predict_x)
    real_predict_array = np.array(predict_y).reshape(data_size, 3)

    return predict_data, real_predict_array


def predict(data_path, model_path):
    data_path = data_path
    data = pd.read_csv(data_path)
    model = tf.keras.models.load_model(model_path+'/학습모델.h5')

    input_data = data.iloc[:, :]
    input_numpy = input_data.to_numpy()[0]
    input_numpy = np.reshape(input_numpy, (len(input_numpy), 1,))
    predict_data = model.predict(input_numpy)
    print("\n")
    print(predict_data)
    Predict = predict_data[0][0]
    print("\n")
    print(Predict)

    return Predict
# %%
