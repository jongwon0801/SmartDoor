<?php
include_once('./_common.php');

define('_INDEX_', true);
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

if(defined('G5_THEME_PATH')) {
    require_once(G5_THEME_PATH.'/index.php');
    return;
}

if (G5_IS_MOBILE) {
    include_once(G5_MOBILE_PATH.'/index.php');
    return;
}

include_once(G5_PATH.'/head.php');
?>


<div id="video_popup">
  <div class="box">
    <iframe width="100%" height="500px;" src="https://www.youtube.com/embed/Hsfngh4SMqs?enablejsapi=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" id="video-player" allowfullscreen></iframe>
    <span class="video_close">X</span>
  </div>
</div>

<nav class="main-page-anchor">
  <ul id="menu">
     <li data-menuanchor="section-page1" class="active"><a href="#section-page1"><span>HOME</span></a></li>
     <li data-menuanchor="section-page2"><a href="#section-page2"><span>주요 기능</span></a></li>
	   <li data-menuanchor="section-page3"><a href="#section-page3"><span>구성</span></a></li>
	   <li data-menuanchor="section-page4"><a href="#section-page4"><span>APP</span></a></li>
	   <li data-menuanchor="section-page5"><a href="#section-page5"><span>활용</span></a></li>
     <li data-menuanchor="section-page6"><a href="#section-page6"><span>경쟁력</span></a></li>
     <li data-menuanchor="section-page7"><a href="#section-page7"><span>보유기술</span></a></li>
     <li data-menuanchor="section-page8"><a href="#section-page8"><span>특허/인증</span></a></li>
     <li data-menuanchor="section-page9"><a href="#section-page9"><span>CONTACT</span></a></li>
  </ul>
</nav>
<div id="fullpage">
  <section class="section page01" id="section0">
  	<div class="vid-info container">
  		<p data-aos="fade-right" data-aos-duration="1500">현명한 <b>집사</b><br>
         든든한 <b>문지기</b><br>
        <img src="/home/img/box01_text.png" alt="wise monster"  id="sl_logo">
        <a href="#" class="video_popup">영상보기 <i class="fa fa-angle-right" aria-hidden="true"></i></a>
  		</p>
  		<img src="/home/img/scr.png" id="scr">
  	</div>
  </section>
  <!-- 주요기능 -->
  <section class="section page02 mob_page0" id="section1">
    	<div class="page_text container">
        <span class="middle"></span>
        <div class="page02_text">
          <h2>전력공급 시스템과 스마트 도어락이 결합된<br><b>아파트용 스마트도어</b></h2>
          <p id="text">상시 전원이 공급 되는 문<br>
          상시 네트워크가 연결 되어있는 문<br>
          스마트 도어락, 도어벨, 카메라, 인포메이션 디스플레이,<br>
          얼굴 인식, 사람감지센서 등 부착</p>
        <ul>
          <li><span class="img"><img src="/home/img/box02_icon01.png" alt="날씨/대기정보"></span>
            <p>날씨/대기정보</p></li>
          <li><span class="img"><img src="/home/img/box02_icon02.png" alt="시간/달력"></span><p>시간/달력</p></li>
          <li><span class="img"><img src="/home/img/box02_icon03.png" alt="실시간 모니터링"></span><p>실시간 모니터링</p></li>
          <li><span class="img"><img src="/home/img/box02_icon04.png" alt="커뮤니케이션"></span><p>커뮤니케이션</p></li>
          <li><span class="img"><img src="/home/img/box02_icon05.png" alt="소지품 알림"></span><p>소지품 알림</p></li>
          <li><span class="img"><img src="/home/img/box02_icon06.png" alt="얼굴 인식"></span><p>얼굴 인식</p></li>
          <li><span class="img"><img src="/home/img/box02_icon07.png" alt="홈 조명 제어"></span><p>홈 조명 제어</p></li>
          <li><span class="img"><img src="/home/img/box02_icon08.png" alt="출입 기록 열람"></span><p>출입 기록 열람</p></li>
          <li><span class="img"><img src="/home/img/box02_icon09.png" alt="게스트 키 생성"></span><p>게스트 키 생성</p></li>
          <li><span class="img"><img src="/home/img/box02_icon10.png" alt="도어락 원격 제어"></span><p>도어락 원격 제어</p></li>
        </ul>
        </div>
        <div class="page02_pro" data-aos="fade-left" data-aos-duration="800"><img src="<?php echo G5_IMG_URL?>/box02_img.png" alt="wisemonster"></div>
    	</div>
  </section>
  <!-- 구성 -->
  <section class="section page03 mob_page1" id="section2">
    <div class="page_text">
      <ul class="door_ul">
      <li class="in">
        <ul class="door_icon">
          <li>
            <span class="img"><img src="/home/img/box03_in01.png" alt="터치 디스플레이"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>터치 디스플레이</h3>
              <p>거울 내 대형 터치<br>
                디스플레이 장착</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_in02.png" alt="얼굴인식"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>얼굴인식</h3>
              <p>인공지능 카메라로<br>
                가족 구성원 자동 인식</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_in03.png" alt="전면 거울"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>전면 거울</h3>
              <p>강화유리로 구성 된 대형 거울</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_in04.png" alt="날씨,대기정보"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>날씨,대기정보</h3>
              <p>외출 전 날씨 및 예보,<br>
                대기 정보 제공</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_in05.png" alt="가족 소통"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>가족 소통</h3>
              <p>등록된 가족 구성원에게<br>
                알림 및 음성 메모 재생</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_in06.png" alt="홈 IOT"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>홈 IOT</h3>
              <p>조명, 가스 벨브, 엘리베이터<br>
                호출 등 제어 기능</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_in07.png" alt="캘린더"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>캘린더</h3>
              <p>시간 및 날짜, 가족 스케줄 공유</p>
            </div>
          </li>
        </ul>
        <img src="/home/img/box03_in_door.png" alt="" class="door_img">
      </li>
      <li class="out">
        <ul class="door_icon">
          <li>
            <span class="img"><img src="/home/img/box03_out01.png" alt="방범모드"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>방범모드</h3>
              <p>외출 시 설정하면<br>
                외부 동작 감지 APP으로 알림</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_out02.png" alt="게스트키 생성"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>게스트키 생성</h3>
              <p>외부인에게 임시로<br>
              출입키 발행</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_out03.png" alt="스마트 벨"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>스마트 벨</h3>
              <p>벨이 울리면 외부에서도<br>
                APP으로 확인 가능</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_out04.png" alt="원격 제어"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>원격 제어</h3>
              <p>외부에서 원격으로 잠금 해제</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_out05.png" alt="외부 감시"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>외부 감시</h3>
              <p>디스플레이 및 APP내에서<br>
                실시간 외부 감시 가능</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_out06.png" alt="출입 기록"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>출입 기록</h3>
              <p>가족 및 손님 방문 기록 확인</p>
            </div>
          </li>
          <li>
            <span class="img"><img src="/home/img/box03_out07.png" alt="예비 전력"></span>
            <span class="middle"></span>
            <div class="text">
              <h3>예비 전력</h3>
              <p>전원 차단 시 예비 전력 구동</p>
            </div>
          </li>
        </ul>
        <img src="/home/img/box03_out_door.png" alt="" class="door_img">
      </li>
    </ul>
    <a href="#" class="arrow left"></a>
   <a href="#" class="arrow right"></a>
    </div>
  </section>
  <!-- app -->
  <section class="section page04 mob_page2" id="section3">
    	<div class="page_text container">
        <div class="left" data-aos="flip-right" data-aos-delay="0" data-aos-duration="500">
          <div class="cont_box">
            <h2>01.</h2>
            <h3>영상 통화</h3>
            <p>외부에 있을 때<br>방문객과 영상 통화</p>
          </div>
          <div class="cont_box">
            <h2>02.</h2>
            <h3>원격제어</h3>
            <p>실시간으로 도어락 원격제어 가능</p>
          </div>
        </div>
        <img src="/home/img/box04_phone.png" alt="">
        <div class="right" data-aos="flip-right" data-aos-delay="300" data-aos-duration="500">
          <div class="cont_box">
            <h2>03.</h2>
            <h3>사운드 키</h3>
            <p>원격으로 임시사용 가능한<br>
              음파 통신 기술을 적용한 키 발행화</p>
          </div>
          <div class="cont_box">
            <h2>04.</h2>
            <h3>방문 기록 확인</h3>
            <p>출입 기록을 간편하게 APP으로 확인</p>
          </div>
        </div>
    	</div>
  </section>
  <!-- 활용 -->
  <section class="section page05 mob_page3" id="section4">
    	<div class="page_text container" data-aos="fade-up" data-aos-duration="800">
          <div class="cont_box">
            <span class="img"><img src="/home/img/box05_01.png" alt=""></span>
            <span class="middle"></span>
            <div class="text">
                <h2>01</h2>
              <h3>외출을 도와주는 스마트 도어</h3>
              <p><span>·</span>자동으로 얼굴을 인식해 필요한 준비물을 알려주는 개인 맞춤 알림<br>
            <span>·</span>스크린을 통해 가족 일정 및 가족이 전하는 메시지를 볼 수 있음<br>
            <span>·</span>스마트도어 대형 스크린을 통해 외부 날씨 및 대기 상황을 알려줌</p>
            </div>
          </div>
          <div class="cont_box">
            <span class="img"><img src="/home/img/box05_02.png" alt=""></span>
            <span class="middle"></span>
            <div class="text">
              <h2>02</h2>
            <h3>외출 후</h3>
            <p><span>·</span>스마트 도어락에 내장된 카메라로 외부에서도 APP을 통해 외부인과 영상통화<br>
            <span>·</span>APP을 사용하여 원격으로 문을 열어줄 수 있음</p>
          </div>
          </div>
          <div class="cont_box">
            <span class="img"><img src="/home/img/box05_03.png" alt=""></span>
            <span class="middle"></span>
            <div class="text">
              <h2>03</h2>
            <h3>보안</h3>
            <p><span>·</span>문 외측에 내장된 동작 감지 센서와 카메라를 통해 외부 상황을 24시간 모니터링<br>
            <span>·</span>문 앞에 움직임이 감지되면 모바일 APP으로 알려주며, APP으로 외부상황 모니터링 및 영상으로 확인할 수 있음<br>
            <span>·</span>외부 상황을 동영상과 사진으로 기록하여 필요하면 언제든 조회할 수 있음
            </p>
          </div>
          </div>
          <div class="cont_box">
            <span class="img"><img src="/home/img/box05_04.png" alt=""></span>
            <span class="middle"></span>
            <div class="text">
              <h2>04</h2>
            <h3>가족간 소통</h3>
            <p><span>·</span>사용자의 얼굴을 자동으로 인식하여 스크린을 통해 가족 간의 메시지 및 중요 행사를 알려줌</p>
          </div>
          </div>
          <div class="cont_box">
            <span class="img"><img src="/home/img/box05_05.png" alt=""></span>
            <span class="middle"></span>
            <div class="text">
              <h2>05</h2>
            <h3>부재 시 부모님/친척이 방문할 때</h3>
            <p><span>·</span>부재 시 손님이 방문 했을때 영상통화로 확인하고 문을 열어 줄 수 있음</p>
          </div>
          </div>

      </div>
  </section>
  <!-- 경쟁력 -->
  <section class="section page06 mob_page4" id="section5">
        <ul class="page06_sl">
        <li class="page06_01">
          <span class="middle"></span>
          <div class="page06_01_text">
              <table class="s_table scroll">
                <colgroup>
                    <col width="7%">
                    <col width="7%">
                    <col width="20%">
                    <col width="20%">
                </colgroup>
                <thead>
                  <th colspan="2">기능</th>
                  <th>기존 방화문</th>
                  <th>와이즈 몬스터<br>스마트 도어</th>
                </thead>
                <tbody>
                  <tr>
                    <th rowspan="3">방화문</th>
                    <th>차연</th>
                    <td>O</td>
                    <td>O</td>
                  </tr>
                  <tr>
                    <th>내화</th>
                    <td>O</td>
                    <td>O</td>
                  </tr>
                  <tr>
                    <th>단열</th>
                    <td>O</td>
                    <td>O</td>
                  </tr>
                  <tr>
                    <th rowspan="5">도어락</th>
                    <th>설치</th>
                    <td>별도 구매, 별도 설치</td>
                    <td>일체형</td>
                  </tr>
                  <tr>
                    <th>전원 공급 방식</th>
                    <td>건전지 교체(1년 주기)</td>
                    <td>전원 상시 공급</td>
                  </tr>
                  <tr>
                    <th>원격제어</th>
                    <td>제한적</td>
                    <td>항시 가능</td>
                  </tr>
                  <tr>
                    <th>게스트키 발급</th>
                    <td>APP 설치 강제</td>
                    <td>미디어 파일 전달</td>
                  </tr>
                  <tr>
                    <th>통신방식</th>
                    <td>블루투스</td>
                    <td>홈 네트워크 연동</td>
                  </tr>
                  <tr>
                    <th colspan="2">편의기능</th>
                    <td>X</td>
                    <td>날씨/대기 알림, 조명제어<br>
                    엘리베이터 호출<br>
                    소지품 알림</td>
                  </tr>
                  <tr>
                    <th colspan="2">보안기능</th>
                    <td>X</td>
                    <td>동작감지, 모니터링<br>
                      출입기록 열람</td>
                  </tr>
                  <tr>
                    <th colspan="2">커뮤니케이션</th>
                    <td>X</td>
                    <td>공지, 메모 전달<br>
                      가족 메신저</td>
                  </tr>
                </tbody>
              </table>
            </div>
        </li>
        <li class="page06_02">
          <span class="middle"></span>
            <div class="page06_02_text">
          <h2>전력공급 시스템이 적용되는 최초의 문</h2>
          <b>IOT 사업자가 참여 할 수 있는 플랫폼 도어</b>
          <p>전기로 부터 자유로워지면 IOT사업자들이 서드 파티(third party) 개발사로 참여 가능하고,<br>
            문에 다양한 기능과 새로운 디바이스를 추가 할 수 있다.</p>
          <b>디스플레이에서 통합 제어</b>
          <p>홈 네트워크를 연동하여 집안의 상황을 확인할 수 있고 제어할 수 있다.</p>
        </div>
        </li>
      </ul>
      <a href="#" class="arrow left"></a>
     <a href="#" class="arrow right"></a>
  </section>
  <!-- 보유기술 -->
  <section class="section page08 mob_page5" id="section8">
      <div class="page_text container" data-aos="fade-up" data-aos-duration="800">
        <div class="tech">
          <h2><img src="/home/img/box08_tit.png" alt="보유기술"></h2>
          <div>
            <img src="/home/img/box08_tech01.png" alt="영상 통신 기술">
            <h3><i class="fas fa-caret-right"></i> 영상 통신 기술</h3>
            <p>별도의 통신장비 없이 인터넷을 통해 도어와<br>
              모바일 APP간의 안정적인 영상 통화 구현 기술 보유</p>
          </div>
          <div>
            <img src="/home/img/box08_tech02.png" alt="음파 통신 기술">
            <h3><i class="fas fa-caret-right"></i> 음파 통신 기술</h3>
            <p>스마트폰에 내장 된 스피커와 마이크를 활용하여<br>
              음파로 키를 생성하고 이를 무선통신 방식으로<br>
              도어락에 전달하는 기술</p>
            <p>모바일 APP 없이 오디오 파일이 도어락의 열쇠<br>
              역할을 하도록 암호화 및 해제하는 기술 보유</p>
          </div>
          <div>
            <img src="/home/img/box08_tech03.png" alt="임베디드 스마트 시스템 구축">
            <h3><i class="fas fa-caret-right"></i> 임베디드 스마트 시스템 구축</h3>
            <p>무선통신, 각종 센서, 대형 스크린, 도어락 등이<br>
              통합되어있는 임베디드 시스템 설계, 구현 기술</p>
            <p>임베디드 시스템을 제어하고 운영할 수 있는<br>
              소프트웨어 개발 능력 보유</p>
          </div>
        </div>
      </div>
  </section>
  <section class="section page09 mob_page6" id="section8">
      <div class="page_text container">
        <div class="cert">
          <h2>특허</h2>
          <ul>
            <li>
              <img src="/home/img/box08_cert.png" alt="" style="border:solid 1px #ccc">
              <p>제 10-2150642호<br>무선충전을 이용한 스마트 도어 시스템</p>
            </li>
            <li>
              <img src="/home/img/box08_cert02.png" alt="" style="border:solid 1px #ccc">
              <p>제 10-0123460호<br>다기능 스마트 도어</p>
          </li>
          </ul>
        </div>
        <div class="cert" style="margin-bottom:0">
          <h2>인증</h2>
          <ul>
            <li><img src="/home/img/box08_cert03.png" alt="" style="border:solid 1px #ccc"><p>KC 인증서</p></li>
            <li><img src="/home/img/box08_cert04.png" alt="" style="border:solid 1px #ccc"><p>방화문 시험성적서</p></li>
            <li><img src="/home/img/box08_cert05.png" alt="" style="border:solid 1px #ccc"><p>방화문 시험성적서</p></li>
          </ul>
        </div>
      </div>
  </section>
  <!-- 컨택트어스 -->
  <section class="section page10 mob_page7" id="section9">
    <div class="cata">
      <img src="/home/img/logo_w.png" alt="wise monster">
      <a href="/home/data/cata.pdf" target="_blank">카탈로그</a>
    </div>
  	<div class="page_text">
      <div class="container">
        <div id="contact_left">
          <h3>CONTACT US</h3>
          <p>Wiki Smartdoor에 관해 궁금한 점이 있으시면 언제든지 문의해 주세요.<br>
            빠른시일내에 답변 드리도록하겠습니다.</p>
          <ul class="info">
            <li>
              <i class="fas fa-building"></i>
              <span>(주)위키박스</span>
            </li>
            <li>
              <i class="fas fa-map-marker-alt"></i>
              <span>경기도 남양주시 다산순환로 20<br>
                다산현대프리미어캠퍼스 B-302호(다산동)</span>
            </li>
            <li>
              <i class="fas fa-headset"></i>
              <span>1577-4594</span>
            </li>
            <li>
              <i class="fas fa-envelope"></i>
              <span>wikibox76417@wikibox.kr</span>
            </li>
          </ul>
        </div>
        <form name="contactform" method="post" action="send.php" id="contact_right">
						<input name="first_name"  type="text" class="ipt" style="height:30px" maxlength="50" required placeholder="이름">
            <input name="email"  type="text" class="ipt" style="height:30px" maxlength="80" required placeholder="이메일주소">
            <input name="telephone"  type="text" class="ipt" style="height:30px"  maxlength="30" required placeholder="연락처">
						<textarea  name="comments" cols="50" rows="10" required placeholder="문의사항"></textarea>
					<input type="checkbox" id="check" name="agree" value="개인정보정책에 동의합니다"  required> 개인정보정책에 동의합니다.
					<p id="pri">
            당사는 상담, 서비스 신청 등을 위해 아래와 같은 개인정보를 수집하고 있습니다.<br>
            1. 수집항목 : 이름 , 연락처, 이메일주소<br>
            2. 개인정보 수집방법 : Wiki Smartdoor 홈페이지 고객문의<br><br>
            개인정보의 수집 및 이용목적<br>
            당사는 수집한 개인정보를 다음의 목적을 위해 활용합니다.<br>
            1. 서비스이용에 따른 본인확인, 개인식별, 불량회원의 부정 이용 방지와 비인가 사용방지, 불만처리 등 민원처리<br>
            2. 서비스 이용에 대한 통계<br><br>
            개인정보의 보유 및 이용기간<br>
            회사는 개인정보 수집 및 이용목적이 달성된 후에는 예외없이 해당 정보를 지체 없이 파기합니다.<br>
          </p>
					<input type="submit" value="보내기" class="btn_submit">
			</form>
      </div>
  	</div><!-- page_text -->
  </section>
  <section class="section page11 fp-auto-height" id="section10">
    	<div class="page_text container">

      </div>
  </section>
  </div>

<script type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>
<script>

	$(document).ready(function(){

        // $(window).resize(function() {
        //     location.reload();
        // });

		$('.gnb li').click(function(){
            if(!$(this).hasClass("mob_close")) {
    			var offset = $(".mob_page"+$(this).index()).offset(); //선택한 태그의 위치를 반환
                //animate()메서드를 이용해서 선택한 태그의 스크롤 위치를 지정해서 0.4초 동안 부드럽게 해당 위치로 이동함
                var pixel = 74;
                if($(this).index()==3) { pixel += 50; }

    	        $('html').animate({scrollTop : offset.top-pixel}, 400);
                $(".site-header .gnb").removeClass('on');
            }
		});
	});
</script>

<?php include_once(G5_PATH.'/_tail.php') ?>
