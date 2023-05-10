FROM "pihole/pihole:2023.03.1"

RUN apt update && apt upgrade -y && apt install -y unbound

COPY unbound-pihole.conf /etc/unbound/unbound.conf.d/pihole.conf
COPY 99-edns.conf /etc/dnsmasq.d/99-edns.conf
RUN mkdir -p /etc/services.d/unbound
COPY unbound-run /etc/services.d/unbound/run

ENTRYPOINT [ "/s6-init" ]