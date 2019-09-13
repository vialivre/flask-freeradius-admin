FROM freeradius/freeradius-server:3.0.19

COPY ./raddb/ /etc/raddb/
COPY ./configs/sql /etc/freeradius/mods-available/sql
RUN ln -s /etc/freeradius/mods-available/sql /etc/freeradius/mods-enabled/sql