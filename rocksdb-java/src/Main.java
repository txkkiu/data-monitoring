import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by koushikkrishnan on 2/6/17.
 */

public class Main {

    public static void main(String[] args) {
        SimpleRocksDB db = new RocksDBBuilder().withPath("~/").build();

        db.set("key", "value");
        System.out.println(db.get("key"));

        Map<String, SubData> data = new HashMap<>();
        data.put("GPA", new SubData("4.00", (new Date()).toString()));
        data.put("Ice Cream", new SubData("Vanilla", (new Date()).toString()));
        InputData test = new InputData(data);

        db.add("Hello", test);

        System.out.println(db.get("Hello"));
        db.delete("Hello");
        if (args.length != 2) {
            System.out.println(String.format("Invalid arguments: %s", Arrays.toString(args)));
        }
    }
}
