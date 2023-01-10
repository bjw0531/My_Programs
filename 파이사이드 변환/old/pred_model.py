# %%  라이브러리 Load
import tensorflow as tf
import numpy as np
import pandas as pd
import datetime
import os
import csv
from keras.layers import Input, Dense
from keras.models import Model
from keras.utils import plot_model
from keras.callbacks import EarlyStopping


def train11(data_path, combo_index):
    # 데이터 Laod--------------------------------------------------------------------------------
    data_path = data_path  # input 데이터 변수
    save_path = data_path

    data = pd.read_csv(data_path)
    data_size = len(data)  # 데이터 행 개수
    if combo_index == 1:
        train_output = "ITEM001"  # 종속변수
        column_name = ['ITEM001', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 2:
        train_output = "ITEM005"  # 종속변수
        column_name = ['ITEM005', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 3:
        train_output = "ITEM009"  # 종속변수
        column_name = ['ITEM009', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 4:
        train_output = "ITEM013"  # 종속변수
        column_name = ['ITEM013', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 5:
        train_output = "ITEM017"  # 종속변수
        column_name = ['ITEM017', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 6:
        train_output = "ITEM021"  # 종속변수
        column_name = ['ITEM021', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 7:
        train_output = "ITEM025"  # 종속변수
        column_name = ['ITEM025', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 8:
        train_output = "ITEM029"  # 종속변수
        column_name = ['ITEM029', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 9:
        train_output = "ITEM033"  # 종속변수
        column_name = ['ITEM033', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 10:
        train_output = "ITEM037"  # 종속변수
        column_name = ['ITEM037', 'ITEM093', 'ITEM094', 'ITEM095',
                       'ITEM096', 'ITEM097', 'ITEM098', 'ITEM099', 'ITEM100']
    elif combo_index == 11:
        train_output = "ITEM043"  # 종속변수
        column_name = ['ITEM043', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 12:
        train_output = "ITEM047"  # 종속변수
        column_name = ['ITEM047', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 13:
        train_output = "ITEM051"  # 종속변수
        column_name = ['ITEM051', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 14:
        train_output = "ITEM055"  # 종속변수
        column_name = ['ITEM055', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 15:
        train_output = "ITEM059"  # 종속변수
        column_name = ['ITEM059', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 16:
        train_output = "ITEM063"  # 종속변수
        column_name = ['ITEM063', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 17:
        train_output = "ITEM067"  # 종속변수
        column_name = ['ITEM067', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 18:
        train_output = "ITEM071"  # 종속변수
        column_name = ['ITEM071', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 19:
        train_output = "ITEM075"  # 종속변수
        column_name = ['ITEM075', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 20:
        train_output = "ITEM079"  # 종속변수
        column_name = ['ITEM079', 'ITEM085', 'ITEM086', 'ITEM087',
                       'ITEM088', 'ITEM089', 'ITEM090', 'ITEM091', 'ITEM092']
    elif combo_index == 21:
        train_output = "ITEM083"  # 종속변수
        column_name = ['ITEM083', 'ITEM101', 'ITEM102', 'ITEM103',
                       'ITEM104', 'ITEM105', 'ITEM106', 'ITEM107', 'ITEM108']

    def get_dataset(file_path, **kwargs):  # CSV 구성
        dataset = tf.data.experimental.make_csv_dataset(
            file_path,
            batch_size=data_size,
            label_name=train_output,
            na_value="?",  # NA / NaN 값의 처리방식 구성
            ignore_errors=True,
            **kwargs)
        return dataset

    raw_data_train = get_dataset(data_path,
                                 select_columns=column_name,
                                 )

    def pack(feartures, label):
        return tf.stack(list(feartures.values()), axis=-1), label

    packed_dataset = raw_data_train.map(pack)
    for feartures, labels in packed_dataset.take(1):
        None

    # 학습, 검증, 평가용 데이터 분류--------------------------------------------------------------------------------
    eval_size = int(data_size/10)
    predict_size = int(data_size/10)
    train_size = data_size - eval_size - predict_size

    train_x, eval_x, predict_x = feartures[:train_size, :], feartures[train_size:train_size +
                                                                      eval_size, :], feartures[data_size-predict_size:, :],
    train_y, eval_y, predict_y = labels[:train_size], labels[train_size:train_size +
                                                             eval_size], labels[data_size-predict_size:]

    # 모델 입력용 데이터 구성
    data_x_array = np.array(feartures)
    data_y_array = np.array(labels).reshape(len(labels), 1)
    data_xy_array = np.concatenate((data_x_array, data_y_array), axis=1)
    dataframe = pd.DataFrame(data_xy_array, columns=column_name)

    # 모델 설계--------------------------------------------------------------------------------
    def make_model():
        initializer = tf.keras.initializers.HeNormal()
        Input1 = Input(8, name='Input_layer')  # 독립변수 개수
        x = Dense(16, activation='relu', name='Hidden_layer1')(Input1)
        x = Dense(32, activation='relu', name='Hidden_layer2')(x)
        x = Dense(64, activation='relu',
                  kernel_initializer=initializer, name='Hidden_layer3')(x)
        x = Dense(32, activation='relu', name='Hidden_layer4')(x)
        x = Dense(16, activation='relu',
                  kernel_initializer=initializer, name='Hidden_layer5')(x)
        output = Dense(1, activation='softplus', name='Output_layer')(x)  # 출력층
        model = Model(inputs=Input1, outputs=output)
        return model

    model = make_model()
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

    Epochs = 50  # 학습 반복횟수
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
    _file = data_path.split('/')[-1]  # modified
    _path = data_path.rstrip(_file)  # modified

    model_path = _path+'/학습모델.h5'
    model.save(model_path)

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
    with open(_path+'/예측결과.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Predicted power", "Actual power",
                        "Abs error", "MAE", "MAPE"])
        writer.writerow(["", "", "", mae, mape])
        for a in range(len(predict_output)):
            writer.writerow(
                [predict_output[a][0], real_predict_array[a][0], predictor_error[a][0]])

    return mse, mae, mape, model_path, predict_output, real_predict_array


def predict(data_path, model_path):
    data_path = data_path
    data = pd.read_csv(data_path)
    model = tf.keras.models.load_model(model_path+'/학습모델.h5')

    input_data = data.iloc[:, :]
    input_numpy = input_data.to_numpy()
    input_numpy = np.reshape(input_numpy, (len(input_data), 8,))
    predict_data = model.predict(input_numpy)
    print("\n")
    print(predict_data)
    Predict = predict_data[0][0]
    print("\n")
    print(Predict)

    return Predict
