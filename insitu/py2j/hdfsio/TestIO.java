package hdfsio;

import java.io.*;

import org.apache.hadoop.conf.*;
import org.apache.hadoop.fs.*;
import org.apache.hadoop.io.*;

public class TestIO {
	private static final long MEGA = 0x100000;
	private static String DATA_DIR = "/data";
	private static byte[] buffer;
	private static final int DEFAULT_BUFFER_SIZE = 1000000;
	private static Configuration fsConfig;
	private static FileSystem fs; 

  TestIO() throws Exception {
    
  }

  public static void main(String[] args) throws Exception{
    // fsConfig = new Configuration();
    // fs = FileSystem.get(fsConfig);
    // fs.delete(new Path(DATA_DIR), true);
    System.out.println("Test HDFS I/O");
    // writeBytes(fs, "a", 2);
  }

  public static void writeHDFS() throws Exception {
    System.out.println("Write HDFS");
    writeBytes("a", 2);
  }


  private static void writeBytes(String name, long totalSize) throws IOException {
  	int bufferSize = DEFAULT_BUFFER_SIZE;
  	buffer = new byte[bufferSize];
  	for(int i=0; i < bufferSize; i++)
    buffer[i] = (byte)('0' + i % 50);
    fsConfig = new Configuration();
    fs = FileSystem.get(fsConfig);

  	// create file
  	totalSize *= MEGA;
  	OutputStream out;
  	out = fs.create(new Path(DATA_DIR, name), true, bufferSize);
  
  	try {
      // write to the file
      long nrRemaining;
      for (nrRemaining = totalSize; nrRemaining > 0; nrRemaining -= bufferSize) {
        int curSize = (bufferSize < nrRemaining) ? bufferSize : (int)nrRemaining; 
        out.write(buffer, 0, curSize);
      }
    } finally {
      out.close();
    }
    // return new Long(totalSize);
  }
}
