FROM freeradius/freeradius-server:3.0.19

COPY ./configs/sql /etc/freeradius/mods-available/sql
RUN ln -s /etc/freeradius/mods-available/sql /etc/freeradius/mods-enabled/sql