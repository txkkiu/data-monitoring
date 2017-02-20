import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * Created by nick on 2/17/17.
 */
public class StoredData {
    private Map<String, StoredHistory> map;

    public StoredData() {
        this.map = new HashMap<>();
    }

    public StoredData(Map<String, SubData> input) {
        this.map = new HashMap<>();
        Set<Map.Entry<String, SubData>> set = input.entrySet();
        for (Map.Entry<String, SubData> pair : set) {
            map.put(pair.getKey(), new StoredHistory(pair.getValue()));
        }
    }

    public Map<String, StoredHistory> getMap() {
        return map;
    }

    public void setMap(Map<String, StoredHistory> map) {
        this.map = map;
    }
}