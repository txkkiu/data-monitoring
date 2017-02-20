import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Created by nick on 2/17/17.
 */
public class StoredHistory {
    private List<SubData> history;

    public StoredHistory() {
        this.history = new ArrayList<>();
    }

    public StoredHistory(SubData data) {
        history = new ArrayList<>();
        history.add(data);
    }

    public List<SubData> getHistory() {
        return history;
    }

    public void setHistory(List<SubData> history) {
        this.history = history;
    }
}
