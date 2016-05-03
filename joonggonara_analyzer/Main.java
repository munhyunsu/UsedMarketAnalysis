/* File */
import java.io.File;
import java.io.IOException;

/* List */
import java.util.List;
import java.util.LinkedList;

/* Regular Expression */
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/* Jsoup: 서드파티 라이브러리 */
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Main {
	/**
	* 메인 메소드
	* 경로를 인자로 받아 그 안에 있는 파일 경로를 String 형태로 저장하는 작업을 진행
	*/
	public static void main(String[] args) {
		// 인자 확인
		// 인자는 경로로 주어져야 함
		if(args.length > 1) {
			SurfFiles(args[0], args[1]);
		} else {
			System.out.println("We need exactly 2 path argument contain privacy files");
			System.exit(0);
		}
	} // end main

	private static void SurfFiles(String src, String des) {
		// 디렉터리를 저장하는 List
		List<String> dirList = new LinkedList<String>();
		// Queue에 디렉터리 저장
		dirList.add(src);
		// 경로에 있는 파일을 읽어와 Loop
		while(dirList.isEmpty() == false) { //isEmpty() - 비어있을 경우 true리턴
			// 경로 Pop
			String targetPath = (String)((LinkedList)dirList).pop();
			File currentFile = new File(targetPath);
			File[] listOfFiles = currentFile.listFiles();

			// 내부 디렉터리 탐색
			for( int i = 0; i < listOfFiles.length; i++ ) {
				if( listOfFiles[i].isFile() == true ) { // 파일 일 경우
					//System.out.println("File: " + listOfFiles[i].getPath());// DEBUG
					parsePrivacy(listOfFiles[i].getPath());
				} else if( listOfFiles[i].isDirectory() == true ) {
					System.out.println("Directory: " + listOfFiles[i].getPath()); // DEBUG
					// 서브 디렉터리 삽입
					dirList.add(listOfFiles[i].getPath());
				} // end if
			} // end for
		} // end while
	} // end SurfFile()


	/**
	* 파일 경로를 인자로 받아 파싱을 하는 메소드
	*/
	private static void parsePrivacy(String path) {
		// document html
		Document html = null;

		// HTML 파일 열기
		try { // 만일을 대비
			// EUC-KR 인코딩으로 읽기
			html = Jsoup.parse(new File(path), "EUC-KR");
		} catch(IOException e) { // 파일이 없을 경우 Exception
			e.printStackTrace();
		}

		// 파싱 시작
		Element temp = null;
		Elements temps = null;
		Pattern reg = null;
		Matcher mat = null;
		// 게시글 번호 파싱
		String article_number = null;
		temp = html.getElementById("linkUrl"); // id="linkUrl" 을 찾음
		temps = temp.getElementsByTag("a"); // <a> </a>를 찾음
		article_number = (temps.first()).text(); // 첫번째 인자를 text()로 가져옴 - linkUrl, a에 Element가 1개
		article_number = (article_number.split("/", 5))[4]; // "/"로 split을 하고 5번째 인자(글번호)를 가지고 옴

		// 게시글 작성 시간 파싱
		String article_time = null;
		temps = html.getElementsByClass("date"); // class="m-tcol-c date"중 date가 전체 문서중 유일 따라서 date로 찾음
		article_time = (temps.first()).text(); // 1개만 검색되어 첫번째 인자를 text()로 가져옴
		if(article_time.length() == 16) {
			article_time = article_time.substring(0, 10) + ". " + article_time.substring(11, 16);
		}

		// 게시글 제목 파싱
		String article_title = null;
		temps = html.getElementsByClass("b") // class="b m-tcol=c"
				.select("span.m-tcol-c:not(.reply)"); // <span> 이며 reply 제외
		article_title = (temps.first()).text(); // 1개만 검색되며 그 중 첫번째가 타이틀
		article_title = article_title.replace("\"", "_");

		// 아이디 파싱
		String header_id = null;
		temps = html.getElementsByClass("m-tcol-c") // class="m-tcol-c b"
				.select("a.b[onclick]"); // <a> 이며 b onclick attr이 있는 것
		header_id = (temps.first()).attr("onclick"); // onclick attribute value를 가져옴
		header_id = (header_id.split("'", 3))[1]; // "'"로 split을 하고 2번째 인자를 가져옴

		// 닉네임 파싱
		String header_nick = null;
		temps = html.getElementsByClass("m-tcol-c") // class="m-tcol-c b"
				.select("a.b[onclick]"); // <a> 이며 b onclick이 있는 것
		header_nick = (temps.first()).text(); // 첫번째의 Text
		header_nick = (header_nick.split("\\(", 2))[0]; // 닉네임(아이디) 형식으로 반환되니 split

		// 이메일 파싱
		String header_email = null;
		temps = html.getElementsByClass("rp") // class="rp"
				.select("a.m-tcol-c:not(.view_contact):not(.view_tel)"); // 파싱
		if(temps.size() != 0) {
			header_email = (temps.first()).text();
		} else {
			header_email = null;
		}

		// 휴대폰 번호 파싱
		String header_phone = null;
		temps = html.getElementsByClass("rp")
				.select("div:not(a):not(span)");
		if(temps.size() != 0) {
			header_phone = (temps.first()).text();
			reg = Pattern.compile("\\d{3}-\\d{3,4}-\\d{4}");
			mat = reg.matcher(header_phone);
			if(mat.find()) {
				header_phone = mat.group(0);
			} else {
				reg = Pattern.compile("\\*{3}-\\*{3,4}-\\*{4}");
				mat = reg.matcher(header_phone);
				if(mat.find()) {
					header_phone = mat.group(0);
				} else {
					header_phone = null;
				}
			}
		} else {
			header_phone = null;
		}
		temp = html.getElementById("bt_showPhoneNo");
		if(temp != null) {
			header_phone = "Protect_Number";
		}

		// 본문
		String body_text = null;
		temps = html.getElementsByClass("NHN_Writeform_Main");
		if(temps.size() != 0) {
			body_text = (temps.first()).text();
		} else {
			temp = html.getElementById("tbody");
			body_text = temp.text();
		}

		// 휴대폰 번호(바디) 파싱
		String body_phone = null;
		reg = Pattern.compile("\\d{3}-\\d{3,4}-\\d{4}");
		mat = reg.matcher(body_text);
		if(mat.find()) {
			body_phone = mat.group(0);
		}
		reg = Pattern.compile("\\d{3}.\\d{3,4}.\\d{4}");
		mat = reg.matcher(body_text);
		if(mat.find()) {
			body_phone = mat.group(0);
		}
		reg = Pattern.compile("\\d{3} \\d{3,4} \\d{4}");
		mat = reg.matcher(body_text);
		if(mat.find()) {
			body_phone = mat.group(0);
		}
		if(body_phone != null) {
			body_phone = body_phone.replace(".", "-");
			body_phone = body_phone.replace(" ", "-");
		}

		// 이베일 주소(		
		String body_email = null;
		reg = Pattern.compile("\\w{5,20}@\\w{4,7}.com");
		mat = reg.matcher(body_text);
		if(mat.find()) {
			body_email = mat.group(0);
		}
		reg = Pattern.compile("\\w{5,20}@\\w{4,7}.co.kr");
		mat = reg.matcher(body_text);
		if(mat.find()) {
			body_email = mat.group(0);
		}



		// DEBUG
		System.out.println("article_number: " + article_number +
			", article_time: " + article_time +
			", article_title: " + article_title +
			", header_id: " + header_id +
			", header_nick: " + header_nick +
			", header_email: " + header_email +
			", header_phone: " + header_phone +
			", body_phone: " + body_phone +
			", body_email: " + body_email);
	}

}
