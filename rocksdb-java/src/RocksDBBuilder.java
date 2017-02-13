import org.rocksdb.RocksDB;
import org.rocksdb.Options;
import org.rocksdb.RocksDBException;


/**
 * Created by koushikkrishnan on 2/7/17.
 */
public class RocksDBBuilder {

    private Options options;
    private String path;

    public RocksDBBuilder() {
        RocksDB.loadLibrary();
        options = new Options().setCreateIfMissing(true);
    }

    public RocksDBBuilder withPath(String path) {
        this.path = path;
        return this;
    }

    public RocksDBBuilder withOptions(Options options) {
        this.options = options;
        return this;
    }

    public SimpleRocksDB build() {
        RocksDB db = null;
        try {
            db = RocksDB.open(options, path);
        } catch (RocksDBException e) {
            e.printStackTrace();
        }
        return new SimpleRocksDB(db);
    }

}
