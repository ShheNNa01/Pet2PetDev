--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: breeds; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.breeds (
    breed_id integer NOT NULL,
    breed_name character varying(30) NOT NULL,
    pet_type_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.breeds OWNER TO postgres;

--
-- Name: breeds_breed_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.breeds_breed_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.breeds_breed_id_seq OWNER TO postgres;

--
-- Name: breeds_breed_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.breeds_breed_id_seq OWNED BY public.breeds.breed_id;


--
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comments (
    comment_id integer NOT NULL,
    post_id integer,
    user_id integer,
    pet_id integer,
    comment text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.comments OWNER TO postgres;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comments_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comments_comment_id_seq OWNER TO postgres;

--
-- Name: comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comments_comment_id_seq OWNED BY public.comments.comment_id;


--
-- Name: followers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.followers (
    follower_id integer NOT NULL,
    follower_pet_id integer,
    followed_pet_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.followers OWNER TO postgres;

--
-- Name: followers_follower_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.followers_follower_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.followers_follower_id_seq OWNER TO postgres;

--
-- Name: followers_follower_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.followers_follower_id_seq OWNED BY public.followers.follower_id;


--
-- Name: friendships; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.friendships (
    friendship_id integer NOT NULL,
    pet_id_1 integer,
    pet_id_2 integer,
    status boolean,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.friendships OWNER TO postgres;

--
-- Name: friendships_friendship_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.friendships_friendship_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.friendships_friendship_id_seq OWNER TO postgres;

--
-- Name: friendships_friendship_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.friendships_friendship_id_seq OWNED BY public.friendships.friendship_id;


--
-- Name: group_comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.group_comments (
    group_comment_id integer NOT NULL,
    group_post_id integer,
    user_id integer,
    pet_id integer,
    comment text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.group_comments OWNER TO postgres;

--
-- Name: group_comments_group_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.group_comments_group_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.group_comments_group_comment_id_seq OWNER TO postgres;

--
-- Name: group_comments_group_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.group_comments_group_comment_id_seq OWNED BY public.group_comments.group_comment_id;


--
-- Name: group_members; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.group_members (
    member_id integer NOT NULL,
    group_id integer,
    user_id integer,
    pet_id integer,
    joined_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    admin boolean
);


ALTER TABLE public.group_members OWNER TO postgres;

--
-- Name: group_members_member_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.group_members_member_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.group_members_member_id_seq OWNER TO postgres;

--
-- Name: group_members_member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.group_members_member_id_seq OWNED BY public.group_members.member_id;


--
-- Name: group_posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.group_posts (
    group_post_id integer NOT NULL,
    group_id integer,
    user_id integer,
    pet_id integer,
    content text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.group_posts OWNER TO postgres;

--
-- Name: group_posts_group_post_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.group_posts_group_post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.group_posts_group_post_id_seq OWNER TO postgres;

--
-- Name: group_posts_group_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.group_posts_group_post_id_seq OWNED BY public.group_posts.group_post_id;


--
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.groups (
    group_id integer NOT NULL,
    name_group character varying(100) NOT NULL,
    description text,
    owner_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    group_picture character varying(255),
    privacy boolean
);


ALTER TABLE public.groups OWNER TO postgres;

--
-- Name: groups_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.groups_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.groups_group_id_seq OWNER TO postgres;

--
-- Name: groups_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.groups_group_id_seq OWNED BY public.groups.group_id;


--
-- Name: media_files; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.media_files (
    media_id integer NOT NULL,
    user_id integer,
    post_id integer,
    group_post_id integer,
    comment_id integer,
    group_comment_id integer,
    media_url character varying(255),
    media_type character varying(50),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.media_files OWNER TO postgres;

--
-- Name: media_files_media_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.media_files_media_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.media_files_media_id_seq OWNER TO postgres;

--
-- Name: media_files_media_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.media_files_media_id_seq OWNED BY public.media_files.media_id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    notification_id integer NOT NULL,
    user_id integer,
    type character varying(100) NOT NULL,
    related_id integer,
    is_read boolean,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    message character varying(500) NOT NULL,
    additional_data json,
    updated_at timestamp with time zone
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- Name: notifications_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notifications_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_notification_id_seq OWNER TO postgres;

--
-- Name: notifications_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notifications_notification_id_seq OWNED BY public.notifications.notification_id;


--
-- Name: pet_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pet_types (
    pet_type_id integer NOT NULL,
    type_name character varying(30) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.pet_types OWNER TO postgres;

--
-- Name: pet_types_pet_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pet_types_pet_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pet_types_pet_type_id_seq OWNER TO postgres;

--
-- Name: pet_types_pet_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pet_types_pet_type_id_seq OWNED BY public.pet_types.pet_type_id;


--
-- Name: pets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pets (
    pet_id integer NOT NULL,
    user_id integer,
    name character varying(50) NOT NULL,
    breed_id integer,
    birthdate date,
    gender character varying(15),
    bio character varying(200),
    pet_picture character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean
);


ALTER TABLE public.pets OWNER TO postgres;

--
-- Name: pets_pet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pets_pet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pets_pet_id_seq OWNER TO postgres;

--
-- Name: pets_pet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pets_pet_id_seq OWNED BY public.pets.pet_id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    post_id integer NOT NULL,
    user_id integer,
    pet_id integer,
    content text,
    location text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- Name: posts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.posts_post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_post_id_seq OWNER TO postgres;

--
-- Name: posts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.posts_post_id_seq OWNED BY public.posts.post_id;


--
-- Name: private_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.private_messages (
    message_id integer NOT NULL,
    sender_pet_id integer,
    receiver_pet_id integer,
    message text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    read_status boolean
);


ALTER TABLE public.private_messages OWNER TO postgres;

--
-- Name: private_messages_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.private_messages_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.private_messages_message_id_seq OWNER TO postgres;

--
-- Name: private_messages_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.private_messages_message_id_seq OWNED BY public.private_messages.message_id;


--
-- Name: reactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reactions (
    reaction_id integer NOT NULL,
    post_id integer,
    user_id integer,
    pet_id integer,
    reaction_type character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.reactions OWNER TO postgres;

--
-- Name: reactions_reaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reactions_reaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reactions_reaction_id_seq OWNER TO postgres;

--
-- Name: reactions_reaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reactions_reaction_id_seq OWNED BY public.reactions.reaction_id;


--
-- Name: reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reports (
    report_id integer NOT NULL,
    reported_by_user_id integer,
    reported_content_id integer,
    reason text,
    status boolean,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.reports OWNER TO postgres;

--
-- Name: reports_report_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reports_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reports_report_id_seq OWNER TO postgres;

--
-- Name: reports_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reports_report_id_seq OWNED BY public.reports.report_id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_role_id_seq OWNER TO postgres;

--
-- Name: roles_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_roles (
    user_role_id integer NOT NULL,
    user_id integer,
    role_id integer,
    assigned_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_roles OWNER TO postgres;

--
-- Name: user_roles_user_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_roles_user_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_roles_user_role_id_seq OWNER TO postgres;

--
-- Name: user_roles_user_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_roles_user_role_id_seq OWNED BY public.user_roles.user_role_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying(100) NOT NULL,
    user_last_name character varying(100) NOT NULL,
    user_city character varying(150),
    user_country character varying(100),
    user_number character varying(20),
    user_email character varying(254) NOT NULL,
    user_bio character varying(500),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    status boolean,
    password character varying(100) NOT NULL,
    profile_picture character varying(255),
    role_id integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: breeds breed_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.breeds ALTER COLUMN breed_id SET DEFAULT nextval('public.breeds_breed_id_seq'::regclass);


--
-- Name: comments comment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments ALTER COLUMN comment_id SET DEFAULT nextval('public.comments_comment_id_seq'::regclass);


--
-- Name: followers follower_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.followers ALTER COLUMN follower_id SET DEFAULT nextval('public.followers_follower_id_seq'::regclass);


--
-- Name: friendships friendship_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friendships ALTER COLUMN friendship_id SET DEFAULT nextval('public.friendships_friendship_id_seq'::regclass);


--
-- Name: group_comments group_comment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_comments ALTER COLUMN group_comment_id SET DEFAULT nextval('public.group_comments_group_comment_id_seq'::regclass);


--
-- Name: group_members member_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_members ALTER COLUMN member_id SET DEFAULT nextval('public.group_members_member_id_seq'::regclass);


--
-- Name: group_posts group_post_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_posts ALTER COLUMN group_post_id SET DEFAULT nextval('public.group_posts_group_post_id_seq'::regclass);


--
-- Name: groups group_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups ALTER COLUMN group_id SET DEFAULT nextval('public.groups_group_id_seq'::regclass);


--
-- Name: media_files media_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_files ALTER COLUMN media_id SET DEFAULT nextval('public.media_files_media_id_seq'::regclass);


--
-- Name: notifications notification_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications ALTER COLUMN notification_id SET DEFAULT nextval('public.notifications_notification_id_seq'::regclass);


--
-- Name: pet_types pet_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pet_types ALTER COLUMN pet_type_id SET DEFAULT nextval('public.pet_types_pet_type_id_seq'::regclass);


--
-- Name: pets pet_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets ALTER COLUMN pet_id SET DEFAULT nextval('public.pets_pet_id_seq'::regclass);


--
-- Name: posts post_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts ALTER COLUMN post_id SET DEFAULT nextval('public.posts_post_id_seq'::regclass);


--
-- Name: private_messages message_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.private_messages ALTER COLUMN message_id SET DEFAULT nextval('public.private_messages_message_id_seq'::regclass);


--
-- Name: reactions reaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reactions ALTER COLUMN reaction_id SET DEFAULT nextval('public.reactions_reaction_id_seq'::regclass);


--
-- Name: reports report_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports ALTER COLUMN report_id SET DEFAULT nextval('public.reports_report_id_seq'::regclass);


--
-- Name: roles role_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);


--
-- Name: user_roles user_role_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN user_role_id SET DEFAULT nextval('public.user_roles_user_role_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
dde9051aea46
\.


--
-- Data for Name: breeds; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.breeds (breed_id, breed_name, pet_type_id, created_at) FROM stdin;
1	Labrador Retriever	9	2024-10-23 17:06:12.009943-05
2	Pastor Alemán	9	2024-10-23 17:06:12.009943-05
3	Bulldog Francés	9	2024-10-23 17:06:12.009943-05
4	Golden Retriever	9	2024-10-23 17:06:12.009943-05
5	Chihuahua	9	2024-10-23 17:06:12.009943-05
6	Pomerania	9	2024-10-23 17:06:12.009943-05
7	Beagle	9	2024-10-23 17:06:12.009943-05
8	Dálmata	9	2024-10-23 17:06:12.009943-05
9	Border Collie	9	2024-10-23 17:06:12.009943-05
10	Shih Tzu	9	2024-10-23 17:06:12.009943-05
11	Rottweiler	9	2024-10-23 17:06:12.009943-05
12	Boxer	9	2024-10-23 17:06:12.009943-05
13	Husky Siberiano	9	2024-10-23 17:06:12.009943-05
14	Dogo Argentino	9	2024-10-23 17:06:12.009943-05
15	Bulldog Inglés	9	2024-10-23 17:06:12.009943-05
16	Doberman	9	2024-10-23 17:06:12.009943-05
17	Persa	10	2024-10-23 17:06:12.009943-05
18	Siamés	10	2024-10-23 17:06:12.009943-05
19	Maine Coon	10	2024-10-23 17:06:12.009943-05
20	Bengalí	10	2024-10-23 17:06:12.009943-05
21	Esfinge	10	2024-10-23 17:06:12.009943-05
22	Ragdoll	10	2024-10-23 17:06:12.009943-05
23	Abisinio	10	2024-10-23 17:06:12.009943-05
24	Británico de Pelo Corto	10	2024-10-23 17:06:12.009943-05
25	Devon Rex	10	2024-10-23 17:06:12.009943-05
26	Chartreux	10	2024-10-23 17:06:12.009943-05
27	Birmano	10	2024-10-23 17:06:12.009943-05
28	Tonkinés	10	2024-10-23 17:06:12.009943-05
29	Canario	11	2024-10-23 17:06:12.009943-05
30	Periquito	11	2024-10-23 17:06:12.009943-05
31	Cacatúa	11	2024-10-23 17:06:12.009943-05
32	Loro Amazona	11	2024-10-23 17:06:12.009943-05
33	Agapornis	11	2024-10-23 17:06:12.009943-05
34	Papagayo Gris	11	2024-10-23 17:06:12.009943-05
35	Ninfa	11	2024-10-23 17:06:12.009943-05
36	Guacamayo	11	2024-10-23 17:06:12.009943-05
37	Cotorra Argentina	11	2024-10-23 17:06:12.009943-05
38	Pinzón Cebra	11	2024-10-23 17:06:12.009943-05
39	Periquito Australiano	11	2024-10-23 17:06:12.009943-05
40	Paloma Mensajera	11	2024-10-23 17:06:12.009943-05
41	Iguana	12	2024-10-23 17:06:12.009943-05
42	Gecko Leopardo	12	2024-10-23 17:06:12.009943-05
43	Pitón Bola	12	2024-10-23 17:06:12.009943-05
44	Dragón Barbudo	12	2024-10-23 17:06:12.009943-05
45	Tortuga de Orejas Rojas	12	2024-10-23 17:06:12.009943-05
46	Boa Constrictor	12	2024-10-23 17:06:12.009943-05
47	Camaleón de Velo	12	2024-10-23 17:06:12.009943-05
48	Serpiente Rey de California	12	2024-10-23 17:06:12.009943-05
49	Tortuga Sulcata	12	2024-10-23 17:06:12.009943-05
50	Conejo Holandés	13	2024-10-23 17:06:12.009943-05
51	Cuy Peruano	13	2024-10-23 17:06:12.009943-05
52	Hámster Sirio	13	2024-10-23 17:06:12.009943-05
53	Rata Dumbo	13	2024-10-23 17:06:12.009943-05
54	Chinchilla	13	2024-10-23 17:06:12.009943-05
55	Hurón	13	2024-10-23 17:06:12.009943-05
56	Erizo Africano	13	2024-10-23 17:06:12.009943-05
57	Jerbo	13	2024-10-23 17:06:12.009943-05
58	Conejo Enano	13	2024-10-23 17:06:12.009943-05
59	Pez Betta	14	2024-10-23 17:06:12.009943-05
60	Guppy	14	2024-10-23 17:06:12.009943-05
61	Pez Ángel	14	2024-10-23 17:06:12.009943-05
62	Disco	14	2024-10-23 17:06:12.009943-05
63	Pez Koi	14	2024-10-23 17:06:12.009943-05
64	Neón	14	2024-10-23 17:06:12.009943-05
65	Pez Globo	14	2024-10-23 17:06:12.009943-05
66	Pez Payaso	14	2024-10-23 17:06:12.009943-05
67	Tetra Cardenal	14	2024-10-23 17:06:12.009943-05
68	Goldfish	14	2024-10-23 17:06:12.009943-05
69	Gallina Rhode Island Red	15	2024-10-23 17:06:12.009943-05
70	Gallina Leghorn	15	2024-10-23 17:06:12.009943-05
71	Pato Pekín	15	2024-10-23 17:06:12.009943-05
72	Pato Muscovy	15	2024-10-23 17:06:12.009943-05
73	Gallina Sussex	15	2024-10-23 17:06:12.009943-05
74	Gallina Wyandotte	15	2024-10-23 17:06:12.009943-05
75	Gallina Plymouth Rock	15	2024-10-23 17:06:12.009943-05
76	Cabra Alpina	16	2024-10-23 17:06:12.009943-05
77	Cabra Boer	16	2024-10-23 17:06:12.009943-05
78	Vaca Jersey	16	2024-10-23 17:06:12.009943-05
79	Oveja Merino	16	2024-10-23 17:06:12.009943-05
80	Vaca Holstein	16	2024-10-23 17:06:12.009943-05
81	Oveja Dorper	16	2024-10-23 17:06:12.009943-05
82	Caballo Árabe	16	2024-10-23 17:06:12.009943-05
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comments (comment_id, post_id, user_id, pet_id, comment, created_at, updated_at) FROM stdin;
1	9	1	1	Hola hola	2024-10-25 18:19:38.207518-05	2024-10-25 18:19:38.207518-05
\.


--
-- Data for Name: followers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.followers (follower_id, follower_pet_id, followed_pet_id, created_at) FROM stdin;
2	3	1	2024-10-25 23:00:02.140518-05
4	2	1	2024-10-25 23:49:00.313894-05
\.


--
-- Data for Name: friendships; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.friendships (friendship_id, pet_id_1, pet_id_2, status, created_at) FROM stdin;
\.


--
-- Data for Name: group_comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.group_comments (group_comment_id, group_post_id, user_id, pet_id, comment, created_at) FROM stdin;
\.


--
-- Data for Name: group_members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.group_members (member_id, group_id, user_id, pet_id, joined_at, admin) FROM stdin;
1	1	1	\N	2024-10-25 22:21:54.802025-05	t
2	2	1	\N	2024-10-25 22:30:19.317979-05	t
3	2	1	1	2024-10-25 23:06:27.780042-05	f
\.


--
-- Data for Name: group_posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.group_posts (group_post_id, group_id, user_id, pet_id, content, created_at) FROM stdin;
\.


--
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.groups (group_id, name_group, description, owner_id, created_at, group_picture, privacy) FROM stdin;
1	Dog Lovers Club	A group for dog lovers to share experiences	1	2024-10-25 22:21:54.802025-05	\N	t
2	Dog Lovers Club	A group for dog lovers to share experiences updated	1	2024-10-25 22:30:19.317979-05	\N	f
\.


--
-- Data for Name: media_files; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media_files (media_id, user_id, post_id, group_post_id, comment_id, group_comment_id, media_url, media_type, created_at) FROM stdin;
1	1	9	\N	\N	\N	media/qrcode-generado.png	image/png	2024-10-24 20:36:53.731735-05
2	\N	9	\N	\N	\N	media/posts\\9_34b72e7a-d0b9-4637-a7d6-57aa36722b67.jpg	image/jpeg	2024-10-24 20:54:15.532271-05
3	3	\N	\N	\N	\N	media/qrcode-generado.png	image/png	2024-10-25 18:09:39.898375-05
4	\N	9	\N	\N	\N	media/posts\\9_934e2b84-4a16-47d5-b533-338705f3796f.jpg	image/jpeg	2024-10-25 18:16:15.883671-05
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (notification_id, user_id, type, related_id, is_read, created_at, message, additional_data, updated_at) FROM stdin;
1	1	new_follower	2	t	2024-10-25 23:49:00.321052-05	La Cotorra ha comenzado a seguir a Rizos de Oro	{"follower_pet_id": 2, "follower_pet_name": "La Cotorra", "follower_pet_picture": null, "followed_pet_id": 1, "followed_pet_name": "Rizos de Oro"}	2024-10-25 23:54:48.81528-05
2	1	system	1	f	2024-10-26 03:21:54.813788-05	Has creado el grupo: Dog Lovers Club	{"group_id": 1, "group_name": "Dog Lovers Club"}	\N
3	1	system	2	f	2024-10-26 03:30:19.331354-05	Has creado el grupo: Dog Lovers Club	{"group_id": 2, "group_name": "Dog Lovers Club"}	\N
4	1	group_member_joined	2	f	2024-10-26 04:06:27.789785-05	Nuevo miembro en el grupo: Dog Lovers Club	{"group_id": 2, "group_name": "Dog Lovers Club", "new_member_id": 1, "pet_id": 1}	\N
\.


--
-- Data for Name: pet_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pet_types (pet_type_id, type_name, created_at) FROM stdin;
9	Perro	2024-10-23 17:06:12.009943-05
10	Gato	2024-10-23 17:06:12.009943-05
11	Ave	2024-10-23 17:06:12.009943-05
12	Reptil	2024-10-23 17:06:12.009943-05
13	Mamífero pequeño	2024-10-23 17:06:12.009943-05
14	Pez	2024-10-23 17:06:12.009943-05
15	Ave de corral	2024-10-23 17:06:12.009943-05
16	Mamífero de corral	2024-10-23 17:06:12.009943-05
\.


--
-- Data for Name: pets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pets (pet_id, user_id, name, breed_id, birthdate, gender, bio, pet_picture, created_at, updated_at, status) FROM stdin;
2	2	La Cotorra	31	2024-10-23	female	I say all	\N	2024-10-24 21:28:31.42456-05	2024-10-24 21:28:31.42456-05	t
1	1	Rizos de Oro	1	2024-10-23	female	fiendly 	uploads/pets\\1_52d7a0c4-1048-456a-8727-3877ef045fe6.jpg	2024-10-23 17:23:06.195382-05	2024-10-25 16:44:35.217867-05	t
3	3	felpuita	50	2024-10-25	female	sobame el conejo	uploads/pets\\3_157d5eb9-fb60-4ba0-94e5-637e4a25bc54.jpg	2024-10-25 17:23:43.628343-05	2024-10-25 22:29:13.12558-05	t
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posts (post_id, user_id, pet_id, content, location, created_at, updated_at) FROM stdin;
1	\N	1	"primer post desde swagger"	"Medellin"	2024-10-24 19:34:35.646169-05	2024-10-24 19:34:35.646169-05
2	\N	1	"primer post desde swagger"	"Medellin"	2024-10-24 19:37:15.326909-05	2024-10-24 19:37:15.326909-05
3	\N	1	"primer post desde swagger"	"Medellin"	2024-10-24 19:37:58.7365-05	2024-10-24 19:37:58.7365-05
4	\N	1	"primer post desde swagger"	"Medellin"	2024-10-24 19:38:41.19101-05	2024-10-24 19:38:41.19101-05
5	\N	1	"primer post desde swagger"	"Medellin"	2024-10-24 19:43:47.908973-05	2024-10-24 19:43:47.908973-05
6	\N	1	"primer post desde swagger"	"Medellin"	2024-10-24 19:46:38.48393-05	2024-10-24 19:46:38.48393-05
7	\N	1	"primer post desde swagger"	"Medellin"	2024-10-24 19:47:03.175975-05	2024-10-24 19:47:03.175975-05
9	1	1	"primer post desde postman"	"Medellin"	2024-10-24 20:36:53.726916-05	2024-10-24 20:36:53.726916-05
\.


--
-- Data for Name: private_messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.private_messages (message_id, sender_pet_id, receiver_pet_id, message, created_at, read_status) FROM stdin;
1	2	1	string	2024-10-24 21:36:19.796003-05	t
2	2	1	Hola perrita	2024-10-24 21:50:34.527213-05	t
\.


--
-- Data for Name: reactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reactions (reaction_id, post_id, user_id, pet_id, reaction_type, created_at, updated_at) FROM stdin;
1	9	1	1	sad	2024-10-25 18:26:04.704717-05	2024-10-25 18:26:04.704717-05
\.


--
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports (report_id, reported_by_user_id, reported_content_id, reason, status, created_at) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (role_id, role_name, created_at) FROM stdin;
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_roles (user_role_id, user_id, role_id, assigned_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, user_name, user_last_name, user_city, user_country, user_number, user_email, user_bio, created_at, updated_at, status, password, profile_picture, role_id) FROM stdin;
1	John	Doe	New York	USA	123456789	johndoe@example.com	I love pets more dogs than cats!	2024-10-23 14:14:42.313953-05	2024-10-23 21:17:33.473685-05	t	$2b$12$HsUAz9ZDES3rOHJxpZCYz.FB3omzgfJg.aWBHHXLE4fGG89CelojC	\N	\N
2	Marta	Chores	Titiribi	USA	123456789	chisme@fresco.com	I love chisme! vé pets	2024-10-24 21:23:20.894043-05	2024-10-24 21:23:20.894043-05	t	$2b$12$4Cy9tLQKjJbSSxMBq9ifXe/tZZ4jSYf4Iuxhxv60S4gHac0.IjXDS	\N	\N
3	Casimiro	Tucuca	Don Matias	USA	123456789	chimba@qk.com	I love qk! vé pets	2024-10-25 17:18:27.171164-05	2024-10-25 22:21:07.727644-05	t	$2b$12$GlNSbflg/Fy9/xLFBMA8IOlbLFlH/LvpKZE9zGt3YyxsGQ8yvk0Aa	\N	\N
\.


--
-- Name: breeds_breed_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.breeds_breed_id_seq', 82, true);


--
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comments_comment_id_seq', 1, true);


--
-- Name: followers_follower_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.followers_follower_id_seq', 4, true);


--
-- Name: friendships_friendship_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.friendships_friendship_id_seq', 1, false);


--
-- Name: group_comments_group_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.group_comments_group_comment_id_seq', 1, false);


--
-- Name: group_members_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.group_members_member_id_seq', 3, true);


--
-- Name: group_posts_group_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.group_posts_group_post_id_seq', 1, false);


--
-- Name: groups_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.groups_group_id_seq', 2, true);


--
-- Name: media_files_media_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.media_files_media_id_seq', 4, true);


--
-- Name: notifications_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notifications_notification_id_seq', 4, true);


--
-- Name: pet_types_pet_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pet_types_pet_type_id_seq', 16, true);


--
-- Name: pets_pet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pets_pet_id_seq', 3, true);


--
-- Name: posts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.posts_post_id_seq', 10, true);


--
-- Name: private_messages_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.private_messages_message_id_seq', 2, true);


--
-- Name: reactions_reaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reactions_reaction_id_seq', 1, true);


--
-- Name: reports_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reports_report_id_seq', 1, false);


--
-- Name: roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_role_id_seq', 1, false);


--
-- Name: user_roles_user_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_roles_user_role_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: breeds breeds_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.breeds
    ADD CONSTRAINT breeds_pkey PRIMARY KEY (breed_id);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- Name: followers followers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.followers
    ADD CONSTRAINT followers_pkey PRIMARY KEY (follower_id);


--
-- Name: friendships friendships_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friendships
    ADD CONSTRAINT friendships_pkey PRIMARY KEY (friendship_id);


--
-- Name: group_comments group_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_comments
    ADD CONSTRAINT group_comments_pkey PRIMARY KEY (group_comment_id);


--
-- Name: group_members group_members_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_members
    ADD CONSTRAINT group_members_pkey PRIMARY KEY (member_id);


--
-- Name: group_posts group_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_posts
    ADD CONSTRAINT group_posts_pkey PRIMARY KEY (group_post_id);


--
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (group_id);


--
-- Name: media_files media_files_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_files
    ADD CONSTRAINT media_files_pkey PRIMARY KEY (media_id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (notification_id);


--
-- Name: pet_types pet_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pet_types
    ADD CONSTRAINT pet_types_pkey PRIMARY KEY (pet_type_id);


--
-- Name: pets pets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_pkey PRIMARY KEY (pet_id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (post_id);


--
-- Name: private_messages private_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.private_messages
    ADD CONSTRAINT private_messages_pkey PRIMARY KEY (message_id);


--
-- Name: reactions reactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reactions
    ADD CONSTRAINT reactions_pkey PRIMARY KEY (reaction_id);


--
-- Name: reports reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (report_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- Name: breeds uq_breeds_breed_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.breeds
    ADD CONSTRAINT uq_breeds_breed_name UNIQUE (breed_name);


--
-- Name: pet_types uq_pet_types_type_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pet_types
    ADD CONSTRAINT uq_pet_types_type_name UNIQUE (type_name);


--
-- Name: roles uq_roles_role_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT uq_roles_role_name UNIQUE (role_name);


--
-- Name: users uq_users_user_email; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_user_email UNIQUE (user_email);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_role_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: breeds breeds_pet_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.breeds
    ADD CONSTRAINT breeds_pet_type_id_fkey FOREIGN KEY (pet_type_id) REFERENCES public.pet_types(pet_type_id) ON DELETE CASCADE;


--
-- Name: comments comments_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id) ON DELETE CASCADE;


--
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: notifications fk_notifications_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT fk_notifications_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: followers followers_followed_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.followers
    ADD CONSTRAINT followers_followed_pet_id_fkey FOREIGN KEY (followed_pet_id) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: followers followers_follower_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.followers
    ADD CONSTRAINT followers_follower_pet_id_fkey FOREIGN KEY (follower_pet_id) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: friendships friendships_pet_id_1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friendships
    ADD CONSTRAINT friendships_pet_id_1_fkey FOREIGN KEY (pet_id_1) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: friendships friendships_pet_id_2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friendships
    ADD CONSTRAINT friendships_pet_id_2_fkey FOREIGN KEY (pet_id_2) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: group_comments group_comments_group_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_comments
    ADD CONSTRAINT group_comments_group_post_id_fkey FOREIGN KEY (group_post_id) REFERENCES public.group_posts(group_post_id) ON DELETE CASCADE;


--
-- Name: group_comments group_comments_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_comments
    ADD CONSTRAINT group_comments_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: group_comments group_comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_comments
    ADD CONSTRAINT group_comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: group_members group_members_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_members
    ADD CONSTRAINT group_members_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(group_id) ON DELETE CASCADE;


--
-- Name: group_members group_members_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_members
    ADD CONSTRAINT group_members_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: group_members group_members_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_members
    ADD CONSTRAINT group_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: group_posts group_posts_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_posts
    ADD CONSTRAINT group_posts_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.groups(group_id) ON DELETE CASCADE;


--
-- Name: group_posts group_posts_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_posts
    ADD CONSTRAINT group_posts_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: group_posts group_posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_posts
    ADD CONSTRAINT group_posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: groups groups_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: media_files media_files_comment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_files
    ADD CONSTRAINT media_files_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES public.comments(comment_id);


--
-- Name: media_files media_files_group_comment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_files
    ADD CONSTRAINT media_files_group_comment_id_fkey FOREIGN KEY (group_comment_id) REFERENCES public.group_comments(group_comment_id);


--
-- Name: media_files media_files_group_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_files
    ADD CONSTRAINT media_files_group_post_id_fkey FOREIGN KEY (group_post_id) REFERENCES public.group_posts(group_post_id);


--
-- Name: media_files media_files_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_files
    ADD CONSTRAINT media_files_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id);


--
-- Name: media_files media_files_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_files
    ADD CONSTRAINT media_files_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: pets pets_breed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_breed_id_fkey FOREIGN KEY (breed_id) REFERENCES public.breeds(breed_id) ON DELETE SET NULL;


--
-- Name: pets pets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: posts posts_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: posts posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: private_messages private_messages_receiver_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.private_messages
    ADD CONSTRAINT private_messages_receiver_pet_id_fkey FOREIGN KEY (receiver_pet_id) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: private_messages private_messages_sender_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.private_messages
    ADD CONSTRAINT private_messages_sender_pet_id_fkey FOREIGN KEY (sender_pet_id) REFERENCES public.pets(pet_id) ON DELETE CASCADE;


--
-- Name: reactions reactions_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reactions
    ADD CONSTRAINT reactions_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES public.pets(pet_id);


--
-- Name: reactions reactions_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reactions
    ADD CONSTRAINT reactions_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(post_id) ON DELETE CASCADE;


--
-- Name: reactions reactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reactions
    ADD CONSTRAINT reactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: reports reports_reported_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_reported_by_user_id_fkey FOREIGN KEY (reported_by_user_id) REFERENCES public.users(user_id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id) ON DELETE CASCADE;


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

