import org.rocksdb.RocksDB;
import org.rocksdb.RocksDBException;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * Created by koushikkrishnan on 2/8/17.
 */
public class SimpleRocksDB {

    private RocksDB db;

    public SimpleRocksDB(RocksDB db) {
        this.db = db;
    }

    public String get(String key) {
        String value = null;
        try {
            if (db.get(key.getBytes()) != null) {
                value = new String(db.get(key.getBytes()));
            }
        } catch (RocksDBException e) {
            e.printStackTrace();
        }
        return value;
    }

    public void set(String key, String value) {
        try {
            db.put(key.getBytes(), value.getBytes());
        } catch (RocksDBException e) {
            e.printStackTrace();
        }
    }

    public void add(String key, InputData input) {
        if (get(key) == null) {
            // Add a fresh one
            StoredData stored = new StoredData(input.getMap());
            set(key, Serializer.toJson(stored));
        } else {
            // Update current values
            StoredData stored = Serializer.fromJson(get(key));
            Set<Map.Entry<String, SubData>> set = input.getMap().entrySet();
            for (Map.Entry<String, SubData> pair : set) {
                StoredHistory current = stored.getMap().get(pair.getKey());
                if (!current.getHistory().get(current.getHistory().size() - 1).getValue().equals(pair.getValue().getValue())) {
                    current.getHistory().add(pair.getValue());
                }
            }
            set(key, Serializer.toJson(stored));
        }
    }

    public void delete(String key) {
        try {
            db.singleDelete(key.getBytes());
        } catch(RocksDBException e) {
            e.printStackTrace();
        }
    }
}
