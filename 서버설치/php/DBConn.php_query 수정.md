#### /home/hizib/php/library/class/DBConn.php

```less
function query($query, $isEcho=false) {
	// 개발용: 쿼리 출력 모드
	if ($isEcho) {
		echo "<pre>실행 쿼리:\n" . $query . "</pre>";
		exit();
	}

	// 비어 있는 쿼리 방지
	if (empty(trim($query))) {
		error_log("⚠️ [DBConn::query] 빈 쿼리가 전달되었습니다.");
		throw new Exception("빈 쿼리를 실행하려고 했습니다."); // 또는 return false;
	}

	// DB 연결 확인
	if (!$this->db_handler) {
		throw new Exception("데이터베이스에 연결이 안되어 있습니다.");
	}

	// 쿼리 실행
	if ($this->type === 'mysql') {
		$result = $this->db_handler->query($query);
	} else {
		throw new Exception("지원되지 않는 데이터베이스입니다.");
	}

	// 실행 실패 시 에러 로그 저장
	if (!$result) {
		$this->__errorMsg__ = $this->db_handler->errno . " : " . $this->db_handler->error;
		error_log("❌ [DBConn::query] 쿼리 오류 발생: " . $this->__errorMsg__);
		error_log("실패한 쿼리: " . $query);
	}

	return $result;
}
