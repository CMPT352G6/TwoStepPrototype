package org.project.cmpt352;

import com.example.cmpt352.R;

import android.os.Bundle;
import android.provider.Settings.Secure;
import android.app.Activity;
import android.app.AlertDialog;
import android.graphics.Color;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends Activity {
	private Button generateB;
	private Button deviceID;
	private EditText password;
	private EditText code;
	private String android_id;
	private hotp HOTPalgorithm;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		HOTPalgorithm = new hotp();
		setContentView(R.layout.activity_main);
		
		generateB = (Button)findViewById(R.id.button1);
		password = (EditText)findViewById(R.id.TextView01);
		password.setTextColor(Color.WHITE);
		code = (EditText)findViewById(R.id.editText);
		android_id = Secure.getString(getBaseContext().getContentResolver(),Secure.ANDROID_ID); 
		deviceID = (Button)findViewById(R.id.idButton);
		
		generateB.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				try{
//				if(code.getText().toString().length()>0){
					int newCode = Integer.parseInt(code.getText().toString());
					String newPassword = getPassword(newCode);
					password.setText(String.valueOf(newPassword));
					code.setText("");
				}
				catch(NumberFormatException e){
					 Toast.makeText(getApplicationContext(), "Please input valid code", Toast.LENGTH_SHORT).show(); 
				}
				
			}
			
		});
		
		setDeviceIDListener();
		
	}

	private String getPassword(int inCode){
		byte[] deviceCode = android_id.getBytes();
		String newPassword="";
		try {
		newPassword = hotp.generateOTP(deviceCode, inCode, 8, false, inCode);
		}
	    catch (Exception e) {
	        System.out.println("Exception = " + e);
	        }
		//to do 
		//edit algorithm
		
		return newPassword;
	}
	
	private void setDeviceIDListener(){
		deviceID.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				new AlertDialog.Builder(MainActivity.this)
                .setTitle("Device ID")
                .setMessage(android_id)
                .setPositiveButton("Confirm", null)
                .show(); 
			}
		});
	}
}
