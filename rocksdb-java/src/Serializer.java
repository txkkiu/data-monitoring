import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public final class Serializer {
    private static Gson gson;

    private static Gson getGson() {
        if (gson == null) {
            gson = new GsonBuilder().setPrettyPrinting().create();
        }
        return gson;
    }

    public static String toJson(Object o) {
        return getGson().toJson(o);
    }

    public static StoredData fromJson(String json) {
        return getGson().fromJson(json, StoredData.class);
    }
}