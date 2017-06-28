package sphereobot;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.TextView;

import java.io.DataOutputStream;
import java.io.IOException;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {

    private static final String LOGTAG = "SPHERE-O-BOT";
    private final UUID MY_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    private final String DEVICE_NAME = "SPHERE-O-BOT";
    private BluetoothDevice device = null;
    private DataOutputStream stream2Bot = null;
    private BluetoothSocket btSocket = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        View imageView = (View)findViewById(R.id.control);
        imageView.setOnTouchListener((v, event) -> {
            if (event.getAction() == MotionEvent.ACTION_DOWN) {
                float scale = Math.min(imageView.getWidth(), imageView.getHeight()) / 2.0f;
                handleTouch(
                        (event.getX() - imageView.getWidth() / 2) / scale,
                        -(event.getY() - imageView.getHeight() / 2) / scale);
                return true;
            }
            return false;
             } );

        connectToDevice();
    }

    private void connectToDevice() {
        // Get the local Bluetooth adapter
        BluetoothAdapter mBtAdapter = BluetoothAdapter.getDefaultAdapter();

        if ( mBtAdapter == null){
            printConnectionInfo("No bluetooth available.");
            return;
        }

        // Get a set of currently paired devices
        Set<BluetoothDevice> pairedDevices = mBtAdapter.getBondedDevices();

        device = null;
        for (BluetoothDevice d : pairedDevices) {
            if (d.getName().equals(DEVICE_NAME)) {
                device = d;
                printConnectionInfo("Found device " + DEVICE_NAME);
                break;
            }
        }
        if ( device == null ){
            printConnectionInfo("Could not find device " + DEVICE_NAME);
            return;
        }

        try {
            btSocket = createBluetoothSocket(device);
            printConnectionInfo("Successfully created socket to device " + DEVICE_NAME);
        } catch (IOException e) {
            printConnectionInfo("Failed to create socket to device " + DEVICE_NAME, e);
            return;
        }

        // Establish the Bluetooth socket connection.
        try {
            btSocket.connect();
            printConnectionInfo("Successfully connected to device " + DEVICE_NAME);
        } catch (IOException e) {
            printConnectionInfo("Failed to connect to device " + DEVICE_NAME, e);

        }
        try {
            stream2Bot = new DataOutputStream(btSocket.getOutputStream());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void printConnectionInfo(String message) {
        printConnectionInfo(message, null);
    }

    private void printConnectionInfo(String message, Exception e) {
        TextView textView = (TextView)findViewById(R.id.infoText);
        textView.setText(message);
        if (e != null) {
            Log.i(LOGTAG, message + ": " + e.getMessage());
        } else {
            Log.i(LOGTAG, message);
        }
    }

    private void disconnect(){
        try {
            stream2Bot.close();
            btSocket.close();
            printConnectionInfo( "Successfully closed connection.");
        } catch (IOException e) {
            printConnectionInfo( "Failed to close connection: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private void sendData(byte data){
        if ( !isConnected()){
            printConnectionInfo( "No connection to device, cannot send data");
            return;
        }
        // Send data
        try {
            stream2Bot.write(data);
            printConnectionInfo( "Successfully sent data: " + data);
        } catch (IOException e) {
            e.printStackTrace();
            printConnectionInfo( "Failed to send data " + data + ": " + e.getMessage());
        }
    }

    /**
     * Creates secure outgoing connecetion with BT device using UUID.
     */
    private BluetoothSocket createBluetoothSocket(BluetoothDevice device) throws IOException {
        return  device.createRfcommSocketToServiceRecord(MY_UUID);

    }

    private void handleTouch(float x, float y) {
        // Debugging
        sendData((byte)42);
    }

    public boolean isConnected() {
        return btSocket != null && stream2Bot != null && btSocket.isConnected();
    }
}
