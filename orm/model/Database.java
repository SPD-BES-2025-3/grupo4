package model;

import java.sql.SQLException;
import com.j256.ormlite.jdbc.JdbcConnectionSource;

public class Database {
    private String databaseName = null;
    private JdbcConnectionSource connection = null;

    public Database(String databaseName) {
        this.databaseName = databaseName;
    }

    public JdbcConnectionSource getConnection() throws SQLException {
        if (databaseName == null) {
            throw new SQLException("database name is null");
        }
        if (connection == null) {
            try {
                String url = "jdbc:postgresql://localhost:5432/" + databaseName;
                String user = "postgres";
                String password = "123456";
                connection = new JdbcConnectionSource(url, user, password);
            } catch (Exception e) {
                System.err.println(e.getClass().getName() + ": " + e.getMessage());
                System.exit(0);
            }
        }
        return connection;
    }

    public void close() {
        if (connection != null) {
            try {
                connection.close();
                this.connection = null;
            } catch (Exception e) {
                System.err.println(e);
            }
        }
    }
}
