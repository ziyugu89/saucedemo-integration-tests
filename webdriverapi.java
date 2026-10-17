package cn.gloryroad;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.WebElement;


public class webdriverapi {

	public static void main(String[] args) {
		// 加载谷歌浏览器的驱动程序
		System.setProperty("webdriver.chrome.driver",
				"D:\\qita\\ZJ\\softtest\\chromedriver_win32\\chromedriver.exe"); 
		//定义驱动器的对象
		WebDriver driver = new ChromeDriver();
		    //打开百度页面
		    driver.get("http://www.baidu.com");
		    //停留1000毫秒
		    try {
		    	Thread.sleep(1000);
		    }
		    catch (InterruptedException e) {
		    	// TODO: handle exception
		    	e.printStackTrace();
			}
	        //打开sogou首页
		    driver.get("http://www.sogou.com");
		    
		    try {
		    	Thread.sleep(1000);
		    }
		    catch (InterruptedException e) {
		    	// TODO: handle exception
		    	e.printStackTrace();
			}
		    //返回上一次访问的百度页面
		    driver.navigate().back();
		    String CurrentPageUrl;
		    //获取当前页面的URL地址
		    CurrentPageUrl=driver.getCurrentUrl();
		   
		    
		    try {
		    	Thread.sleep(1000);
		    }
		    catch (InterruptedException e) {
		    	// TODO: handle exception
		    	e.printStackTrace();
			}
		    //从百度页面跳转到搜狗页面
		    driver.navigate().forward();
	                   //定义搜狗文本框的对象
		    WebElement input=driver.findElement(By.id("query"));
		  //清空文本框的内容
		    input.clear();
		    try {
		    	Thread.sleep(1000);
		    }
		    catch (InterruptedException e) {
		    	// TODO: handle exception
		    	e.printStackTrace();
			}
		    //搜索输入框中输入“自动化测试”		    
		    input.sendKeys("自动化测试");
	                   //单击搜索按钮
		    driver.findElement(By.id("stb")).click();
		    try {
		    	Thread.sleep(2000);
		    }
		    catch (InterruptedException e) {
		    	// TODO: handle exception
		    	e.printStackTrace();
			}
		    	    		    
		    
		    //获取页面的title
		    String title = driver.getTitle();
	                   System.out.printf(title);
	 
	                  driver.close();

	}

}

