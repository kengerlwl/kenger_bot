curl -X POST "https://xiaoai.plus/v1/completions" \
-H "Accept: */*" \
-H "Accept-Language: en-US,en;q=0.9,hi;q=0.8" \
-H "Authorization: sk-WJ0m5VzvxGAM18AQXRpH0KE8GHm7ukG7cbw29GGQDQYitM8R" \
-H "Connection: keep-alive" \
-H "Content-Type: application/json" \
-H "Origin: https://platform.openai.com" \
-H "Referer: https://platform.openai.com/" \
-H "Sec-Fetch-Dest: empty" \
-H "Sec-Fetch-Mode: cors" \
-H "Sec-Fetch-Site: same-site" \
-H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36" \
-H "sec-ch-ua: \"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"" \
-H "sec-ch-ua-mobile: ?0" \
-H "sec-ch-ua-platform: \"macOS\"" \
-d '{"prompt": "Your input text here»,\n<|disc_score|>", "max_tokens": 1, "temperature": 1, "top_p": 1, "n": 1, "logprobs": true, "stop": "\n", "stream": false, "model": "gpt-3.5-turbo"}'