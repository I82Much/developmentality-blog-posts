import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ScrambleSolver {
	private final String[][] tiles;
  private List<String> dictionary;
  
  public ScrambleSolver(String[][] tiles, List<String> dictionary) {
    this.tiles = tiles;
    this.dictionary = dictionary;
  }
  
  public List<Solution> solve() {
    List<Solution> solutions = new ArrayList<Solution>();
    
    
    
    
    return solutions;
  }
  
  public static class Solution {
    private String word;
    private List<Location> locations;
    
    public String toString() {
      return word + " " + locations;
    }
  }
  
  public static class Location {
    int column;
    int row;
    
    public String toString() {
      return "(" + row + ", " + column + ")";
    }
  }
  
  
  public static void main(String[] args) throws java.io.FileNotFoundException {
    if (args.length != 1) {
      System.out.println("Usage: java ScrambleSolver /path/to/dict");
    }
    List<String> dictionary = new ArrayList<String>();
    Scanner s = new Scanner(new File(args[0]));
    while(s.hasNextLine()) {
        String line = s.nextLine();
        dictionary.add(line);
    }
    System.out.println(dictionary);
 
    String[][] tiles = {
      {"h", "e", "a", "l"},
      {"h", "e", "l", "l"},
      {"h", "e", "l", "o"},
      {"h", "e", "l", "l"}
    };
    
    ScrambleSolver solver = new ScrambleSolver(tiles, dictionary);
    List<Solution> solutions = solver.solve();
    System.out.println(solutions);
 
  }

}