FROM ocaml/opam:debian-11-ocaml-4.14
ENV LANG C.UTF-8

RUN opam remote add grew "http://opam.grew.fr"
RUN opam install grew

RUN sudo apt-get -qy --no-install-recommends install python3 pip

RUN sudo pip3 install flask gunicorn sklearn

EXPOSE 8200

WORKDIR /home/aconeil

CMD gunicorn -w 2 server:main -b 0.0.0.0
