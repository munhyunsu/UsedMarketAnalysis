/* List */
import java.util.List;
import java.util.LinkedList;
/* File */
import java.io.File;
import java.io.IOException;

/* Files */
import java.nio.file.Files;
import static java.nio.file.StandardCopyOption.*;
import java.nio.file.Path;
import java.nio.file.Paths;

/* Jsoup: 서드파티 라이브러리 */
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Main {
	/**
	* 테스트용 메인 함수
	*/
	public static void main(String[] args) {
		if(args.length > 1) {
			SurfFiles(args[0], args[1]);
			//System.out.println("Hello, World!! " + args[0]);
		} else {
			System.out.println("인자가 2개 필요합니다.");
			System.out.println("JAVA [SRC] [DES]");
			//System.out.println("Hello, World!");
		}
	} // end void main

	/**
	* 디렉터리 서치
	*/
	private static void SurfFiles(String src, String des) {
		List<String> dirList = new LinkedList<String>();
		dirList.add(src);
		while( dirList.isEmpty() != true ){
			String targetPath = (String)((LinkedList)dirList).pop();
			File currentFile = new File(targetPath);
			File[] listOfFiles = currentFile.listFiles();
			for( int i = 0; i < listOfFiles.length; i++ ) {
				if( listOfFiles[i].isFile() == true ) {
					// System.out.println("File: " + listOfFiles[i].getPath());
					String article_time = ParseJoonggonara(listOfFiles[i].getPath());
					String year = article_time.substring(0, 4);
					String month = article_time.substring(5, 7);
					String day = article_time.substring(8, 10);
					//System.out.println( year +"\t"+month+"\t"+day );

					Path srcPath = Paths.get( listOfFiles[i].getPath() );
					Path desDir = Paths.get( des + "/" + year + "/" + month + "/" + day );
					Path desPath = Paths.get( des + "/" + year + "/" + month + "/" + day + "/" + listOfFiles[i].getName() );
					try {
						Files.createDirectories(desDir);
					} catch(IOException e) { // 만일을 위한 Exception
						e.printStackTrace();
					}
					try{ 
						//Files.copy(srcPath, desPath, REPLACE_EXISTING);
						Files.move(srcPath, desPath);
					} catch(IOException e) { // 만일을 위한 Exception
						e.printStackTrace();
					}
					
				} else if( listOfFiles[i].isDirectory() == true ) {
					System.out.println("Directory: " + listOfFiles[i].getPath());
					dirList.add(listOfFiles[i].getPath());
				} // end if
			} // end for
		} // end while dirList empty
	} // end void SurfFiles

	/**
	* 중고나라 HTML 파싱
	*/
	private static String ParseJoonggonara(String filePath) {
		/* 파싱 변수 */
		Document html = null;

		/* EUC-KR 로 오픈 */
		try{
			html = Jsoup.parse(new File(filePath), "EUC-KR");
		} catch(IOException e) { // 만일을 위한 Exception
			e.printStackTrace();
		}

		/* 게시글 시간 Get */
		String article_time = null;
		Elements temps = null;
		try{
			temps = html.getElementsByClass("date"); // class="m-tcol-c date"중 date가 전체 문서중 유일함, 따라서 date로 검색
			article_time = (temps.first()).text();
		} catch(NullPointerException e) {
			article_time = "1989.06.08.";
			e.printStackTrace();
		}

		/* 게시글 시간 반환 */
		return article_time;
	} // String ParseJoonggonara(String filePath)


} // end Class Main


