create table user(
	uid varchar(10) primary key,
	email varchar(50) not null,
	password  varchar(40) not null, #SHA1 value
	nickname varchar(20) not null,
	introduction varchar(200) not null,

	posts_count int(8) not null,
	follows_count int(8) not null,
	fans_count int(8) not null,

	regdate datetime not null,
	active tinyint(1) not null,
	UNIQUE (email),
	UNIQUE (nickname)
);

create table post(
	pid varchar(16) primary key,
	uid varchar(10) not null,
	posttime datetime not null,
	device varchar(20) not null,
	
	posttext varchar(200) not null,
	rid varchar(16) not null,
	withpic varchar(1200) not null

	praises_count int(8) not null,
	comments_count int(8) not null,
	reposts_count int(8) not null,

	hits int(8) default 0,

	index(posttime),
	foreign key(uid) references user(uid) on delete cascade
	#foreign key(rid) references post(pid),
);

create table comment(
	cid varchar(16) primary key,
	pid varchar(16) not null,
	uid varchar(10) not null,
	commenttime datetime not null,
	commenttext varchar(200) not null,

	index(commenttime),
	foreign key(uid) references user(uid) on delete cascade,
	foreign key(pid) references post(pid) on delete cascade
);


create table repost(
	rid varchar(16) not null,
	pid varchar(16) not null,
	reposttime datetime not null,
	primary key(rid,pid),
	index(reposttime),
	foreign key(rid) references post(pid) on delete cascade,
	foreign key(pid) references post(pid)
);

create table praise(
	pid varchar(16) not null,
	uid varchar(10) not null,
	praisetime datetime not null,
	primary key(pid,uid),
	index(praisetime),
	foreign key(uid) references user(uid) on delete cascade,
	foreign key(pid) references post(pid) on delete cascade
);

create table follow(
	uid varchar(10) not null, # user
	fid varchar(10) not null, # user's focus
	followtime datetime not null,
	primary key(uid,fid),
	index(followtime),
	foreign key(uid) references user(uid) on delete cascade,
	foreign key(fid) references user(uid) on delete cascade
);


DELIMITER $

# trigger for counting praise amount
CREATE TRIGGER praises_autoincrease
AFTER INSERT ON praise
FOR EACH ROW
BEGIN
	UPDATE post SET praises_count = (SELECT COUNT(*) FROM praise WHERE praise.pid = new.pid) WHERE post.pid = new.pid;
END;
$
CREATE TRIGGER praises_autodecrease
AFTER DELETE ON praise
FOR EACH ROW
BEGIN
	UPDATE post SET praises_count = (SELECT COUNT(*) FROM praise WHERE praise.pid = old.pid) WHERE post.pid = old.pid;
END;
$

# trigger for counting comment amount
CREATE TRIGGER comments_autoincrease
AFTER INSERT ON comment
FOR EACH ROW
BEGIN
	UPDATE post SET comments_count = (SELECT COUNT(*) FROM comment WHERE comment.pid = new.pid) WHERE post.pid = new.pid;
END;
$
CREATE TRIGGER comments_autodecrease
AFTER DELETE ON comment
FOR EACH ROW
BEGIN
	UPDATE post SET comments_count = (SELECT COUNT(*) FROM comment WHERE comment.pid = old.pid) WHERE post.pid = old.pid;
END;
$

# trigger for counting repost amount
CREATE TRIGGER reposts_autoincrease
AFTER INSERT ON repost
FOR EACH ROW
BEGIN
	UPDATE post SET reposts_count = (SELECT COUNT(*) FROM repost WHERE repost.pid = new.pid) WHERE post.pid = new.pid;
END;
$
CREATE TRIGGER reposts_autodecrease
AFTER DELETE ON repost
FOR EACH ROW
BEGIN
	UPDATE post SET reposts_count = (SELECT COUNT(*) FROM repost WHERE repost.pid = old.pid) WHERE post.pid = old.pid;
END;
$

# combine fans and follows
CREATE TRIGGER fansfollows_autoincrease
AFTER INSERT ON follow
FOR EACH ROW
BEGIN
	UPDATE user SET follows_count = (SELECT COUNT(*) FROM follow WHERE follow.uid = new.uid) WHERE user.uid = new.uid;
	UPDATE user SET fans_count = (SELECT COUNT(*) FROM follow WHERE follow.fid = new.fid) WHERE user.uid = new.fid;
END;
$

CREATE TRIGGER fansfollows_autodecrease
AFTER DELETE ON follow
FOR EACH ROW
BEGIN
	UPDATE user SET follows_count = (SELECT COUNT(*) FROM follow WHERE follow.uid = old.uid) WHERE user.uid = old.uid;
	UPDATE user SET fans_count = (SELECT COUNT(*) FROM follow WHERE follow.fid = old.fid) WHERE user.uid = old.fid;
END;
$


# trigger for counting post amount
CREATE TRIGGER posts_autoincrease
AFTER INSERT ON post
FOR EACH ROW
BEGIN
	UPDATE user SET posts_count = (SELECT COUNT(*) FROM post WHERE post.uid = new.uid) WHERE user.uid = new.uid;
END;
$
CREATE TRIGGER posts_autodecrease
AFTER DELETE ON post
FOR EACH ROW
BEGIN
	UPDATE user SET posts_count = (SELECT COUNT(*) FROM post WHERE post.uid = old.uid) WHERE user.uid = old.uid;
END;
$