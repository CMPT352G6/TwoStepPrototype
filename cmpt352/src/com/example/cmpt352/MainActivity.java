package com.example.cmpt352;

import android.os.Bundle;
import android.provider.Settings.Secure;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends Activity {
	private Button generateB;
	private Button deviceID;
	private TextView password;
	private EditText code;
	private String android_id;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		generateB = (Button)findViewById(R.id.button1);
		password = (TextView)findViewById(R.id.TextView01);
		code = (EditText)findViewById(R.id.editText);
		android_id = Secure.getString(getBaseContext().getContentResolver(),Secure.ANDROID_ID); 
		deviceID = (Button)findViewById(R.id.idButton);
		
		generateB.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				int newCode = Integer.parseInt(code.getText().toString());
				int newPassword = getPassword(newCode);
				password.setText(String.valueOf(newPassword));
				code.setText("");
				System.out.println("~~~~~~~~~~~"+android_id);
			}
			
		});
		
		setDeviceIDListener();
		
	}

	private int getPassword(int inCode){
		int newPassword;
		//to do 
		//edit algorithm
		newPassword = inCode*12/15;
		
		return newPassword;
	}
	
	private void setDeviceIDListener(){
		deviceID.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				AlertDialog builder = new AlertDialog.Builder(MainActivity.this)
                .setTitle("Device ID")
                .setMessage(android_id)
                .setPositiveButton("Confirm", null)
                .show(); 
			}
		});
	}
}
