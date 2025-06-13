```less
<?php
if (!defined('_GNUBOARD_')) exit; // 개별 페이지 접근 불가

if(defined('G5_THEME_PATH')) {
    require_once(G5_THEME_PATH.'/tail.php');
    return;
}

if (G5_IS_MOBILE) {
    include_once(G5_MOBILE_PATH.'/tail.php');
    return;
}
?>

</div>
<!-- } 콘텐츠 끝 -->
<div class="ft">
<iframe
  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3160.5572291665935!2d127.14917117531837!3d37.61257842148763!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x357b638f348c3135%3A0xd389562f2812a33f!2zKOyjvCnsnITtgqTrsJXsiqQ!5e0!3m2!1sko!2skr!4v1749788262671!5m2!1sko!2skr"
  width="100%" height="450" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0">
</iframe>

  <footer>
    <p>© 2020 Wiki Smartdoor. All rights reserved.</p>
  </footer>
</div>

<!-- } 하단 끝 -->

<?php
include_once(G5_PATH."/tail.sub.php");
?>

```
