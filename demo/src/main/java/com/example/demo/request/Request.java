package com.example.demo.request;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

@Data
public class Request {
    //パラメータ
	@JsonProperty("str")
	private String str;
    
}
