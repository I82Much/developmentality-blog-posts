import java.util.Scanner;

public class ScrambleSolver {
  
  
	private final String[][] tiles;
  private List<String> dictionary;
  
  public static void main(String[] args) {
    if (args.length != 1) {
      System.out.println("Usage: java ScrambleSolver /path/to/dict")
    }
    List<String> dictionary = new ArrayList<String>();
    Scanner s = new Scanner(args[0]);
    while(s.hasNextLine()) {
        String line = s.nextLine();
        dictionary.add(line);
    }
    System.out.println(dictionary);
    
    
  }

}