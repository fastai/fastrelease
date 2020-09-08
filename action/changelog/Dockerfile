FROM fastai/octokit
RUN pip3 install fastrelease
COPY action.sh /
COPY pr.js /
RUN chmod u+x /action.sh
ENTRYPOINT [ "/action.sh" ]
