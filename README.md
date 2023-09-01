# **Alice: 112신고 음성기반 주소완성 및 코드 분류 서비스**
**<2023 데이터 청년 캠퍼스 한국외국어대학교 출품작>**
**언어모델 기반 개체명 인식 기술을 활용한 112 신고 음성기반 주소완성 및 코드 분류 서비스로, 신고자의 음성에서  
피해장소를 인식하고 해당 주소에 대한 구체적인 정보와 전체 발화에서 상황을 파악하여 코드를 제공합니다.**
<br>

## 서비스 소개 


## 데이터 모델 소개



### **주요 파일 설명**
+ **"service/views.py"**
  + main code가 작성된 파일입니다.
  + 이 코드는 사용자로부터 오디오 파일을 받아, 그 내용을 분석하고 분류하여 특정 작업을 수행한 후 결과를 반환합니다.(실제 녹음할 경우 사용되는 부분입니다.)
+ **"stt.py"**
  + 이 코드는 Hugging Face의 Model Hub에 있는 모델에 WAV 파일을 전송하여 결과를 받아오는 코드입니다. (음성파일로 전달할 때 사용되는 파일입니다.)
  + WAV 파일을 읽어 API에 POST 요청을 보내고, 그 응답을 반환합니다.
+ **"ner.py"**
  + Hugging Face의 transformers를 이용해 학습시킨 NER 모델을 로드하고, 사용자의 문장 입력에 따라 개체명을 인식하여 결과를 출력하는 코드입니다.
  + 데이터같은 경우 ① KLUE-BERT 데이터 ② 2018 네이버 NLP 챌린지 데이터 ③ 자체구축 데이터로 이루어져 있습니다.
  + 자체구축 데이터의 경우에는 깃허브 내 madedata.txt파일로 존재합니다.

### **개발 환경**
+ **" 공용 컨테이너 환경인 goorm ide에서 개발을 진행하였습니다."** 
  
### **실행 방법**
+ python은 3.11version 사용하였습니다. 터미널에 들어가셔서 아래와 같은 절차를 따라주시면 됩니다**
  + git clone https://github.com/201803854/Alice
  + cd Alice
  + pip install -r requirements.txt
  + python manage.py runserver localhost:8000
  + localhost:8000/service/mymap  페이지에 들어가셔서 사용하시면 됩니다
  
### **실행 도중 주의사항**
 + 오디오 파일은 .wav만 가능합니다
 + STT 모델이 Loading되는 시간이 있어 1분정도는 실행에 에러가 날 수 있습니다.
  
### **requirements를 설치하는 도중 발생하는 에러모음**
+ Window 환경에서 발생한 에러 모음들입니다.
  + ① ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory:  
  + http://ngmsoftware.com/bbs/board.php?bo_table=study&wr_id=428&sfl=mb_id%2C1&stx=admin&sst=wr_nogood&sod=desc&sop=and&page=4
  
  + ② AttributeError: tuype object 'ImageDraw' has no attribute 'textsize
  + python3 -m pip list -v
  + python3 -c "import PIL;print(PIL.__version__)"
  + 만약 버전이 10.0이라면, 다운그레이드 해주시면 됩니다
  + python3 -m pip install Pillow==9.5.0

  + ③ WARNING: The script huggingface-cli.exe is installed in 'C:\Users\이동현\' which is not on PATH. Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  + 시작 버튼을 마우스 오른쪽 버튼으로 클릭하고 '시스템'을 선택합니다.
  + 오른쪽에 있는 '고급 시스템 설정'을 클릭합니다.
  + '시스템 속성' 창 하단의 '환경 변수'를 클릭합니다.
  + '사용자 변수' 아래에서 PATH 변수를 찾아 '편집'을 클릭합니다.
  + 새로 만들기'를 클릭한 다음 디렉토리 경로를 붙여 넣습니다.
  + 확인을 눌러 변경 사항을 저장합니다.
