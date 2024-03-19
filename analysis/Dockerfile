# Start from the PyTorch image
FROM nvcr.io/nvidia/pytorch:23.10-py3

# Copy the requirements file into the image
COPY requirements.txt .

# Install dependencies from the requirements file
RUN pip install -r requirements.txt

# Start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$BM5f6z8PxSwwx7RenVUb4Q$AWjm2iQ0hS7Rw0pzdj+vFdKyMPaeCZVVzaWdnCESArc'"]