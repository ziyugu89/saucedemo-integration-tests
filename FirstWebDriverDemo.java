package cn.gloryroad;

//引入谷歌驱动器类
import org.openqa.selenium.chrome.ChromeDriver;

public class FirstWebDriverDemo {
	public static void main(String[] args) {
		// 加载谷歌浏览器的驱动程序
		System.setProperty("webdriver.chrome.driver", "D:\\seleweb\\chromedriver_win32\\chromedriver.exe"); 
		ChromeDriver driver = new ChromeDriver();
	        //打开华东理工网站首页
	        driver.get("http://www.ecust.edu.cn");
	        //获取页面的title
	        String title = driver.getTitle();
	        System.out.printf(title);
	        //关闭当前页面
	        driver.close();

	}

}
