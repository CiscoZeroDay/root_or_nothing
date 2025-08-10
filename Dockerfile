FROM ubuntu:24.04

# Changer les miroirs lents vers un miroir rapide
#RUN sed -i 's|http://archive.ubuntu.com/ubuntu|http://mirror.hetzner.com/ubuntu|g' /etc/apt/sources.list

#Install dependencies
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    echo "Etc/UTC" > /etc/timezone && \
    apt-get update && \
    apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    openssh-server \
    nano \
    wget \
    build-essential \
    net-tools \
    coreutils \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*


# Installer sudo vulnérable 1.9.15p5
RUN wget https://www.sudo.ws/dist/sudo-1.9.15p5.tar.gz && \
    tar xvf sudo-1.9.15p5.tar.gz && \
    cd sudo-1.9.15p5 && \
    ./configure && make && make install && \
    cd .. && rm -rf sudo-1.9.15p5 sudo-1.9.15p5.tar.gz

# Vérifie la version de sudo installée
RUN /usr/local/bin/sudo --version

    #create users
RUN useradd -m -s /bin/bash tyrellwellick && \
    echo 'tyrellwellick:@reyou1or0?' | chpasswd && \
    echo 'root:@sfsftsf-/**fs135323**13s1fsfs' | chpasswd

    # Donne les droits à tyrellwellick sur tout son home
RUN chown -R tyrellwellick:tyrellwellick /home/tyrellwellick


    #configure SSH : Enable root login via SSH for testing purposes
RUN mkdir /var/run/sshd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config 

#Set Up Sudo Permissions: Allow the tyrellwellick user to run the nano command as root without a password.
RUN echo 'tyrellwellick ALL=(root) NOPASSWD: /bin/nano' >> /etc/sudoers


# Copy the web application files : copy app flask
WORKDIR /app
COPY . /app

#installer les dépendances
RUN apt-get update && apt-get install -y python3-flask python3-markupsafe && rm -rf /var/lib/apt/lists/*


#Expose ports
EXPOSE 22 80 5000

#Create Flags:Create flags for the tyrellwellick and root users
RUN echo 'DP{Tyre11_W311ick_flag}' > /home/tyrellwellick/user.txt && \
    chown tyrellwellick:tyrellwellick /home/tyrellwellick/user.txt && \
    chmod 600 /home/tyrellwellick/user.txt

RUN echo 'DP{Congratu1a710n_H4CKER}' > /root/root.txt && \
    chmod 600 /root/root.txt

# Lancer SSH et Flask (Flask sur 0.0.0.0:5000)
CMD ["/bin/bash", "-c", "/usr/sbin/sshd -D & flask run --host=0.0.0.0 --port=5000"]

