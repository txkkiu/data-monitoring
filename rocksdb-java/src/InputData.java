import java.util.HashMap;
import java.util.Map;

/**
 * Created by nick on 2/17/17.
 */
public class InputData {
    private Map<String, SubData> map;

    public InputData(Map<String, SubData> map) {
        this.map = map;
    }

    public InputData() {
        this.map = new HashMap<>();
    }

    public Map<String, SubData> getMap() {
        return map;
    }

    public void setMap(Map<String, SubData> map) {
        this.map = map;
    }
}