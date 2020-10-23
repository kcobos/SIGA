--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.12
-- Dumped by pg_dump version 9.6.7

-- Started on 2018-06-09 11:28:53 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 186 (class 1259 OID 25973)
-- Name: acreditacion; Type: TABLE; Schema: public; Owner: carlos
--

CREATE TABLE acreditacion (
    uid character varying(100) NOT NULL
);


ALTER TABLE acreditacion OWNER TO carlos;

--
-- TOC entry 212 (class 1259 OID 36343)
-- Name: destino_activo; Type: TABLE; Schema: public; Owner: carlos
--

CREATE TABLE destino_activo (
    id_ubicacion bigint NOT NULL,
    token character(255) NOT NULL
);


ALTER TABLE destino_activo OWNER TO carlos;

--
-- TOC entry 211 (class 1259 OID 36341)
-- Name: destino_activo_id_ubicacion_seq; Type: SEQUENCE; Schema: public; Owner: carlos
--

CREATE SEQUENCE destino_activo_id_ubicacion_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE destino_activo_id_ubicacion_seq OWNER TO carlos;

--
-- TOC entry 3615 (class 0 OID 0)
-- Dependencies: 211
-- Name: destino_activo_id_ubicacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: carlos
--

ALTER SEQUENCE destino_activo_id_ubicacion_seq OWNED BY destino_activo.id_ubicacion;


--
-- TOC entry 213 (class 1259 OID 36361)
-- Name: destino_usuarios; Type: TABLE; Schema: public; Owner: carlos
--

CREATE TABLE destino_usuarios (
    latitud double precision NOT NULL,
    longitud double precision NOT NULL,
    tiempo timestamp without time zone NOT NULL
);


ALTER TABLE destino_usuarios OWNER TO carlos;

--
-- TOC entry 210 (class 1259 OID 36336)
-- Name: historico_plaza; Type: TABLE; Schema: public; Owner: carlos
--

CREATE TABLE historico_plaza (
    tiempo timestamp without time zone NOT NULL,
    id_plaza bigint NOT NULL,
    estado integer
);


ALTER TABLE historico_plaza OWNER TO carlos;

--
-- TOC entry 185 (class 1259 OID 17783)
-- Name: plaza; Type: TABLE; Schema: public; Owner: carlos
--

CREATE TABLE plaza (
    id bigint NOT NULL,
    estado integer NOT NULL,
    id_ubicacion bigint NOT NULL
);


ALTER TABLE plaza OWNER TO carlos;

--
-- TOC entry 184 (class 1259 OID 17781)
-- Name: plaza_id_seq; Type: SEQUENCE; Schema: public; Owner: carlos
--

CREATE SEQUENCE plaza_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE plaza_id_seq OWNER TO carlos;

--
-- TOC entry 3616 (class 0 OID 0)
-- Dependencies: 184
-- Name: plaza_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: carlos
--

ALTER SEQUENCE plaza_id_seq OWNED BY plaza.id;


--
-- TOC entry 188 (class 1259 OID 25984)
-- Name: ubicacion; Type: TABLE; Schema: public; Owner: carlos
--

CREATE TABLE ubicacion (
    id bigint NOT NULL,
    direccion character varying(300) NOT NULL,
    latitud double precision NOT NULL,
    longitud double precision NOT NULL,
    plazas_totales smallint NOT NULL,
    plazas_ocupadas smallint NOT NULL,
    observaciones character varying(150),
    geom geometry(Point,4326)
);


ALTER TABLE ubicacion OWNER TO carlos;

--
-- TOC entry 187 (class 1259 OID 25982)
-- Name: ubicacion_id_seq; Type: SEQUENCE; Schema: public; Owner: carlos
--

CREATE SEQUENCE ubicacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ubicacion_id_seq OWNER TO carlos;

--
-- TOC entry 3617 (class 0 OID 0)
-- Dependencies: 187
-- Name: ubicacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: carlos
--

ALTER SEQUENCE ubicacion_id_seq OWNED BY ubicacion.id;


--
-- TOC entry 3474 (class 2604 OID 36346)
-- Name: destino_activo id_ubicacion; Type: DEFAULT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY destino_activo ALTER COLUMN id_ubicacion SET DEFAULT nextval('destino_activo_id_ubicacion_seq'::regclass);


--
-- TOC entry 3472 (class 2604 OID 17786)
-- Name: plaza id; Type: DEFAULT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY plaza ALTER COLUMN id SET DEFAULT nextval('plaza_id_seq'::regclass);


--
-- TOC entry 3473 (class 2604 OID 25987)
-- Name: ubicacion id; Type: DEFAULT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY ubicacion ALTER COLUMN id SET DEFAULT nextval('ubicacion_id_seq'::regclass);


--
-- TOC entry 3482 (class 2606 OID 36340)
-- Name: historico_plaza historico_plazas_pkey; Type: CONSTRAINT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY historico_plaza
    ADD CONSTRAINT historico_plazas_pkey PRIMARY KEY (tiempo, id_plaza);


--
-- TOC entry 3478 (class 2606 OID 36367)
-- Name: acreditacion pk_acreditacion; Type: CONSTRAINT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY acreditacion
    ADD CONSTRAINT pk_acreditacion PRIMARY KEY (uid);


--
-- TOC entry 3484 (class 2606 OID 36360)
-- Name: destino_activo pk_destino_activo; Type: CONSTRAINT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY destino_activo
    ADD CONSTRAINT pk_destino_activo PRIMARY KEY (id_ubicacion, token);


--
-- TOC entry 3486 (class 2606 OID 36369)
-- Name: destino_usuarios pk_destino_usuarios; Type: CONSTRAINT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY destino_usuarios
    ADD CONSTRAINT pk_destino_usuarios PRIMARY KEY (latitud, longitud, tiempo);


--
-- TOC entry 3476 (class 2606 OID 17788)
-- Name: plaza plazas_pkey; Type: CONSTRAINT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY plaza
    ADD CONSTRAINT plazas_pkey PRIMARY KEY (id);


--
-- TOC entry 3480 (class 2606 OID 25989)
-- Name: ubicacion ubicacion_pkey; Type: CONSTRAINT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY ubicacion
    ADD CONSTRAINT ubicacion_pkey PRIMARY KEY (id);


--
-- TOC entry 3488 (class 2606 OID 36354)
-- Name: historico_plaza fk_id_plaza; Type: FK CONSTRAINT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY historico_plaza
    ADD CONSTRAINT fk_id_plaza FOREIGN KEY (id_plaza) REFERENCES plaza(id);


--
-- TOC entry 3489 (class 2606 OID 36349)
-- Name: destino_activo fk_id_ubicacion; Type: FK CONSTRAINT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY destino_activo
    ADD CONSTRAINT fk_id_ubicacion FOREIGN KEY (id_ubicacion) REFERENCES ubicacion(id);


--
-- TOC entry 3487 (class 2606 OID 25990)
-- Name: plaza ubicacion_fkey; Type: FK CONSTRAINT; Schema: public; Owner: carlos
--

ALTER TABLE ONLY plaza
    ADD CONSTRAINT ubicacion_fkey FOREIGN KEY (id_ubicacion) REFERENCES ubicacion(id);


-- Completed on 2018-06-09 11:28:53 CEST

--
-- PostgreSQL database dump complete
--

