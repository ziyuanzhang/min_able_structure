export const request = async (url: string, method: string, data = {}) => {
  const obj = {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "X-api-Key": "adfsafdafasdfasdfsadf"
    }
  };
  if (method === "POST") {
    obj.body = JSON.stringify(data);
  }
  // console.log(url, obj);
  const response = await fetch("/api" + url, obj);
  // console.log("response:", response);
  try {
    const res = await response.json();
    return res.date ? res.date : res;
  } catch (error) {
    return { error: error };
  }
};

export const get = (url: string, params = {}) => {
  const queryString = new URLSearchParams(params).toString();
  const fullUrl = queryString ? `${url}?${queryString}` : url;
  return request(fullUrl, "GET");
};
export const post = (url: string, data = {}) => {
  return request(url, "POST", data);
};
