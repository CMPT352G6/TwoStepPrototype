package com.example.cmpt352;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends Activity {
	private Button generateB;
	private TextView password;
	private EditText code;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		generateB = (Button)findViewById(R.id.button1);
		password = (TextView)findViewById(R.id.TextView01);
		code = (EditText)findViewById(R.id.editText);
		
		generateB.setOnClickListener(new OnClickListener(){

			@Override
			public void onClick(View v) {
				int newCode = Integer.parseInt(code.getText().toString());
				int newPassword = getPassword(newCode);
				password.setText(String.valueOf(newPassword));
			}
			
		});
	}

	private int getPassword(int inCode){
		int newPassword;
		//to do 
		//edit algorithm
		newPassword = inCode*12/15;
		
		return newPassword;
	}
}
