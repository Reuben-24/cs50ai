Initially Included just a single convolution layer and a single pooling layer with the following arguments:
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

- This seemed to be very inaccurate, resulting in the following results:
    accuracy: 0.0568 
    loss: 3.4953


Added 2 more convolution and pooling layers, doubling the number of filters for each additional layer:
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2, 2)),

- This saw huge improvements in accuracy, these were the results:
accuracy: 0.9814
loss: 0.0675