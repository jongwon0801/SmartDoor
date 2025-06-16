#### /home/hizib/php/library/class/Component.php
```less
# Component.php delete 함수 변경

function delete($json='') {
	global $_lib;

	if(is_string($json)) $json = jsondecode($json);
	if(empty($json)) $json = new stdClass();
	if(is_array($json)) $json = (object) $json;

	// 🛡️ 방어 코드 추가
	if (empty($this->__tableName__) || empty($this->__pkName__) || !isset($this->__pkValue__)) {
		error_log("❌ 삭제 실패: 필수 정보 누락 (table: {$this->__tableName__}, pk: {$this->__pkName__}, value: {$this->__pkValue__})");
		$this->__errorMsg__ = "삭제를 위한 필수 정보가 누락되었습니다.";
		return false;
	}

	$sql = "DELETE FROM ".$this->__tableName__." WHERE ".$this->__pkName__."=".$this->__pkValue__;
	
	if (!empty($json->isEcho)) {
		echo '<xmp>'.$sql.'</xmp>';
		exit();
	}

	if (!isset($_lib['db']['handler']['master'])) {
		$_lib['db']['handler']['master'] = new DBConn($_lib['db']['master']);
	}

	$result = $_lib['db']['handler']['master']->query($sql);

	if (!$result) {
		$this->__errorMsg__ = $this->__tableName__.'의 '.$this->__pkValue__.' 삭제실패';
		return false;
	}

	return true;
}
