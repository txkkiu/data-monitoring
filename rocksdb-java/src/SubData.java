/**
 * Represents a subvalue and date of modification
 * Created by nick on 2/17/17.
 */
public class SubData {
    private String value;
    private String modifiedDate;

    public SubData(String value, String modifiedDate) {
        this.value = value;
        this.modifiedDate = modifiedDate;
    }

    public String getValue() {
        return value;
    }
}