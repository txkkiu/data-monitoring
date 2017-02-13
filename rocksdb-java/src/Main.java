/**
 * Created by koushikkrishnan on 2/6/17.
 */

public class Main {

    public static void main(String[] args) {
        SimpleRocksDB db = new RocksDBBuilder().withPath("~/").build();
        db.set("key", "value");
        System.out.println(db.get("key"));
    }
}
