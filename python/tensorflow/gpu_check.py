import tensorflow as tf
print(str(tf.test.is_gpu_available())) # True/False

# Or only check for gpu's with cuda support
print(str(tf.test.is_gpu_available(cuda_only=True)))