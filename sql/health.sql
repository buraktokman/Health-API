PGDMP     ,    4                {            iatros    15.2    15.2 +    J           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            K           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            L           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            M           1262    16390    iatros    DATABASE     �   CREATE DATABASE iatros WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = icu LOCALE = 'en_US.UTF-8' ICU_LOCALE = 'en-US';
    DROP DATABASE iatros;
                burak    false            �            1259    16498    appointments    TABLE     �   CREATE TABLE public.appointments (
    id integer NOT NULL,
    doctor_id integer NOT NULL,
    patient_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL
);
     DROP TABLE public.appointments;
       public         heap    burak    false            �            1259    16497    appointments_id_seq    SEQUENCE     �   CREATE SEQUENCE public.appointments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.appointments_id_seq;
       public          burak    false    223            N           0    0    appointments_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.appointments_id_seq OWNED BY public.appointments.id;
          public          burak    false    222            �            1259    16469    doctors    TABLE     �  CREATE TABLE public.doctors (
    id integer NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    specialty integer NOT NULL,
    profile_picture character varying(255),
    personal_statement text,
    date_added timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    date_modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.doctors;
       public         heap    burak    false            �            1259    16468    doctors_id_seq    SEQUENCE     �   CREATE SEQUENCE public.doctors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.doctors_id_seq;
       public          burak    false    219            O           0    0    doctors_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.doctors_id_seq OWNED BY public.doctors.id;
          public          burak    false    218            �            1259    16458    patients    TABLE     �  CREATE TABLE public.patients (
    id integer NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    email character varying(255),
    phone_number character varying(255),
    date_of_birth date,
    date_added timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    date_modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.patients;
       public         heap    burak    false            �            1259    16457    patients_id_seq    SEQUENCE     �   CREATE SEQUENCE public.patients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.patients_id_seq;
       public          burak    false    217            P           0    0    patients_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.patients_id_seq OWNED BY public.patients.id;
          public          burak    false    216            �            1259    16486    shifts    TABLE     �   CREATE TABLE public.shifts (
    id integer NOT NULL,
    doctor_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL
);
    DROP TABLE public.shifts;
       public         heap    burak    false            �            1259    16485    shift_id_seq    SEQUENCE     �   CREATE SEQUENCE public.shift_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.shift_id_seq;
       public          burak    false    221            Q           0    0    shift_id_seq    SEQUENCE OWNED BY     >   ALTER SEQUENCE public.shift_id_seq OWNED BY public.shifts.id;
          public          burak    false    220            �            1259    16449 	   specialty    TABLE     {   CREATE TABLE public.specialty (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text
);
    DROP TABLE public.specialty;
       public         heap    burak    false            �            1259    16448    specialty_id_seq    SEQUENCE     �   CREATE SEQUENCE public.specialty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.specialty_id_seq;
       public          burak    false    215            R           0    0    specialty_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.specialty_id_seq OWNED BY public.specialty.id;
          public          burak    false    214            �           2604    16501    appointments id    DEFAULT     r   ALTER TABLE ONLY public.appointments ALTER COLUMN id SET DEFAULT nextval('public.appointments_id_seq'::regclass);
 >   ALTER TABLE public.appointments ALTER COLUMN id DROP DEFAULT;
       public          burak    false    223    222    223            �           2604    16472 
   doctors id    DEFAULT     h   ALTER TABLE ONLY public.doctors ALTER COLUMN id SET DEFAULT nextval('public.doctors_id_seq'::regclass);
 9   ALTER TABLE public.doctors ALTER COLUMN id DROP DEFAULT;
       public          burak    false    218    219    219            �           2604    16461    patients id    DEFAULT     j   ALTER TABLE ONLY public.patients ALTER COLUMN id SET DEFAULT nextval('public.patients_id_seq'::regclass);
 :   ALTER TABLE public.patients ALTER COLUMN id DROP DEFAULT;
       public          burak    false    217    216    217            �           2604    16489 	   shifts id    DEFAULT     e   ALTER TABLE ONLY public.shifts ALTER COLUMN id SET DEFAULT nextval('public.shift_id_seq'::regclass);
 8   ALTER TABLE public.shifts ALTER COLUMN id DROP DEFAULT;
       public          burak    false    220    221    221            �           2604    16452    specialty id    DEFAULT     l   ALTER TABLE ONLY public.specialty ALTER COLUMN id SET DEFAULT nextval('public.specialty_id_seq'::regclass);
 ;   ALTER TABLE public.specialty ALTER COLUMN id DROP DEFAULT;
       public          burak    false    214    215    215            G          0    16498    appointments 
   TABLE DATA           W   COPY public.appointments (id, doctor_id, patient_id, start_time, end_time) FROM stdin;
    public          burak    false    223   �0       C          0    16469    doctors 
   TABLE DATA           �   COPY public.doctors (id, first_name, last_name, specialty, profile_picture, personal_statement, date_added, date_modified) FROM stdin;
    public          burak    false    219   G1       A          0    16458    patients 
   TABLE DATA           |   COPY public.patients (id, first_name, last_name, email, phone_number, date_of_birth, date_added, date_modified) FROM stdin;
    public          burak    false    217   �2       E          0    16486    shifts 
   TABLE DATA           E   COPY public.shifts (id, doctor_id, start_time, end_time) FROM stdin;
    public          burak    false    221   �3       ?          0    16449 	   specialty 
   TABLE DATA           :   COPY public.specialty (id, name, description) FROM stdin;
    public          burak    false    215   �3       S           0    0    appointments_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.appointments_id_seq', 29, true);
          public          burak    false    222            T           0    0    doctors_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.doctors_id_seq', 17, true);
          public          burak    false    218            U           0    0    patients_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.patients_id_seq', 3, true);
          public          burak    false    216            V           0    0    shift_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.shift_id_seq', 3, true);
          public          burak    false    220            W           0    0    specialty_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.specialty_id_seq', 5, true);
          public          burak    false    214            �           2606    16503    appointments appointments_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.appointments DROP CONSTRAINT appointments_pkey;
       public            burak    false    223            �           2606    16478    doctors doctors_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.doctors
    ADD CONSTRAINT doctors_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.doctors DROP CONSTRAINT doctors_pkey;
       public            burak    false    219            �           2606    16467    patients patients_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.patients DROP CONSTRAINT patients_pkey;
       public            burak    false    217            �           2606    16491    shifts shift_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.shifts
    ADD CONSTRAINT shift_pkey PRIMARY KEY (id);
 ;   ALTER TABLE ONLY public.shifts DROP CONSTRAINT shift_pkey;
       public            burak    false    221            �           2606    16456    specialty specialty_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.specialty
    ADD CONSTRAINT specialty_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.specialty DROP CONSTRAINT specialty_pkey;
       public            burak    false    215            �           2606    16504 (   appointments appointments_doctor_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(id);
 R   ALTER TABLE ONLY public.appointments DROP CONSTRAINT appointments_doctor_id_fkey;
       public          burak    false    219    3495    223            �           2606    16509 )   appointments appointments_patient_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);
 S   ALTER TABLE ONLY public.appointments DROP CONSTRAINT appointments_patient_id_fkey;
       public          burak    false    217    223    3493            �           2606    16479    doctors doctors_specialty_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.doctors
    ADD CONSTRAINT doctors_specialty_fkey FOREIGN KEY (specialty) REFERENCES public.specialty(id);
 H   ALTER TABLE ONLY public.doctors DROP CONSTRAINT doctors_specialty_fkey;
       public          burak    false    215    3491    219            �           2606    16492    shifts shift_doctor_id_fkey    FK CONSTRAINT     ~   ALTER TABLE ONLY public.shifts
    ADD CONSTRAINT shift_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(id);
 E   ALTER TABLE ONLY public.shifts DROP CONSTRAINT shift_doctor_id_fkey;
       public          burak    false    221    219    3495            G   @   x�32�44�4�4202�50�50T04�2 !1C����zC��M��-1�aQo5?F��� ���      C   �  x��S�n�0<S_��^�)+��I��������בH����חR����Co$g���G%n�ш���(J��6���>�i�y���������)��~fg��[��Xt:��>0i���`{��F2�9(�N�<�з���(��*-T*�e[4m��%�J�J�b���!_7�#���;6��y2�0��l���хL����4wl(�td��  �s���7F��^X�DB��C���@��O�1��bG����/>�#��4~8�>�Г_EA7�5�7��8�
�?}�Y-���a�{k����=�;���(��fD�1�C�Ң�b�*�J�I�Q��3T'�����������yu[�BZT��ɚ��*�Kh��"+�n���Ŏ<ol���b�WK��(�}�$�Os�8      A   �   x��ͽ�0����*��ӜsJ-e�gsupq���|K�����c��.��8B9��:�o9<���8��YL�=!Y!1H������2����N���о�b��y�$�wy�r���I2pn�W�������b�yJ{��ě��VJ� �?Qt      E   3   x�3�44�4202�50�50T0��20 "d1Cs���b,�M�c���� &�      ?   �   x�}�MN�0���)|�Q%�N �9�lLcZK�S�nQoO��;����o�G��%�q�Q�D�(��2EX���	�����̗� 2�R�� (\	=�����؊FR��m�,N*�����\������40&��xe��֚�E����BhT9В�>p\R.ry�����M�����L;��ͬ�E�Eq�>�wO��J-���P�͵��>��	���     