// import React from "react";
import api from "./axios";

export const getResponsePost = async (url, data, headers) => {
  try {
    const response = await api.post(url, data, {
      headers: headers,
    });
    return response;
  } catch (err) {
    return err;
  }
};

export const getResponseGet = async (url, headers) => {
  try {
    const response = await api.get(url, {
      headers: headers,
    });
    return response;
  } catch (err) {
    return err;
  }
};

export const getResponseDelete = async (url, headers) => {
  try {
    const response = await api.delete(url, {
      headers: headers,
    });
    return response;
  } catch (err) {
    return err;
  }
};

export const getResponsePut = async (url, data, headers) => {
  try {
    const response = await api.put(url, JSON.stringify(data), {
      headers: headers,
    });
    return response;
  } catch (err) {
    return err;
  }
};
