KEY_PASS=pass
STORE_PASS=password
KEY_STORE_NAME=data/keystore.jks

key_gen:
	python3 libs/keystore_libs.py

generate_data:
	mkdir messages
	echo "message1" > messages/m1
	echo "message2" > messages/m2
	echo "message3" > messages/m3

encrypt:
	python3 task_1.py enc \
	--input_folder=messages \
	--output_folder=cyphers

decrypt:
	python3 task_1.py dec \
	--input_folder=cyphers \
	--output_folder=decrypted

generate_challenge_data:
	mkdir challenge
	echo "message1" > challenge/m1
	echo "message2" > challenge/m2

encrypt_challenge:
	python3 task_1.py enc --challenge \
	--input_folder=challenge \
	--output_folder=challenge_out

make clean:
	rm -r challenge challenge_out messages cyphers decrypted
