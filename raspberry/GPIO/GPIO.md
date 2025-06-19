### GPIO pin guide
https://fishpoint.tistory.com/7687

### RPI 4 GPIO

<img src="https://github.com/user-attachments/assets/344cb615-6496-4323-bb1d-123ddd6c8798" width="400" style="margin-bottom:20px;" />


<p float="left">
  <img src="https://github.com/user-attachments/assets/feedc055-5004-41a6-8460-db5514742a67" width="388" height="550" style="margin-right:10px;" />
  <img src="https://github.com/user-attachments/assets/a9f02c43-dc55-465b-9e40-8cf96da47c85" width="388" height="550" />
</p>




#### GPIO(General Purpose Input/Output)
```less
- GPIO(General Purpose Input/Output)는 라즈베리 파이에서 외부 장치와 연결하고 제어하는 데 사용되는 핀들입니다.
- GPIO 핀은 다양한 입출력 작업을 처리할 수 있어, 라즈베리 파이를 다양한 전자기기와 연결하여 제어할 수 있습니다.
```
#### GPIO의 역할
```less
- 1 입력(Input): GPIO 핀을 입력으로 설정하여 외부 장치(예: 버튼, 센서 등)에서 신호를 받아올 수 있습니다.
- 예를 들어, 버튼을 눌렀을 때 GPIO 핀의 상태가 변경되면, 라즈베리 파이는 그 신호를 감지하여 반응할 수 있습니다.

- 2 출력(Output): GPIO 핀을 출력으로 설정하여 라즈베리 파이에서 외부 장치(예: LED, 모터 등)를 제어할 수 있습니다.
예를 들어, GPIO 핀을 통해 LED를 켜거나, 모터를 돌릴 수 있습니다.

- 3 PWM(Pulse Width Modulation): 일부 GPIO 핀은 PWM을 지원하여, 모터의 속도나 조명의 밝기를 조절하는 데 사용할 수 있습니다.
PWM은 신호의 주기를 제어하여 아날로그 신호처럼 동작하게 만드는 디지털 기술입니다.
```
```less
예시
- 버튼 입력: 버튼을 GPIO 핀에 연결하고, 버튼을 누를 때 라즈베리 파이가 그 신호를 감지해 특정 작업을 실행하도록 할 수 있습니다.
- LED 출력: GPIO 핀에 LED를 연결하여, 라즈베리 파이가 해당 핀을 통해 전류를 흐르게 해 LED를 켜거나 끌 수 있습니다.
- 모터 제어: GPIO 핀을 통해 모터의 방향을 바꾸거나 속도를 조절할 수 있습니다.
```
#### GPIO 핀의 수
```less
- 라즈베리 파이에는 다양한 모델이 있으며, 각 모델마다 GPIO 핀의 수가 다를 수 있습니다.
일반적으로 라즈베리 파이에는 40개 핀이 있으며, 그 중 일부는 전원, GND(접지) 및 특수 기능을 제공합니다.

- 나머지 핀들은 입력/출력 용도로 사용됩니다.
```

#### 결론
```less
라즈베리 파이의 GPIO 핀은 외부 장치와 라즈베리 파이 사이에서 데이터를 주고받거나 제어하는 데 중요한 역할을 하며,
전자 회로를 만들고 다양한 프로젝트를 할 수 있는 기반이 됩니다.
```




