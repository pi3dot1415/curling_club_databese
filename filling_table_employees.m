load("cumulative.mat")
load("names.mat")

Positions=["Trainer","Referee","Dietican","Accountant","Assistant","Guard","Cleaner","Manager"];
Sallaries=[35000,38000,42000,27000,24000,22000,21000,120000;6,8,9,5,4,4,3,18];
Sallaries1=[];
Sallaries2=[];
No_position=[8,2,1,2,1,2,2,1];
Employees_position=[""];
Employees_position2=[""];
k=0;

for i=1:length(No_position)
    for j=1:No_position(i)
        Employees_position(j+k)=Positions(i);
        Sallaries1(j+k)=Sallaries(1,i)+randi([0,Sallaries(2,i)])*500;
    end
    k=k+j;
end

r=randperm(sum(No_position));

for i=1:sum(No_position)
    Sallaries2(i)=Sallaries1(r(i));
    Employees_position2(i)=Employees_position(r(i));
end

Sex_l=["Female", "Male"];

first_name=[""];
last_name=[""];
Sex=[""];
phone=[0];
birth_date=[datetime(1962,1,1,'Format','yyyy-MM-dd')];
e_mail=[""];
emp_position=[""];
sallary=[0];
n1=table(first_name,last_name,birth_date,sallary,emp_position,e_mail,phone);

Sallary_pos=[];
numbers=[];
t1 = datetime(1962,1,1,'Format','yyyy-MM-dd');
t2 = datetime(2002,6,19,'Format','yyyy-MM-dd');
time_vector = t1:t2;
domains=["@home.se","@altavista.se","@sverige.mu","@loggain.net","@gmail.com"];

for i=1:sum(No_position)
    r1=rand;
    r2=rand;
    r3=rand;
    i4=0;
    while i4==0
        r4=randi([200000000,999999999],1,1);
        if ismember (r4, numbers)==0
            i4=r4;
            numbers(i)=r4;
        end
    end
    i1=find(r1-0.00001<cumulative(:,(r3<0.5)+1),1,'first');
    i2=find(r2-0.00001<cumulative(:,3),1,'first');
    i3=(r3<0.5)+1;
    r5=randi(length(time_vector),1,1);
    r_time = time_vector(r5);
    t_cell = cellstr(r_time);
    email=make_an_email(char(names{i1,i3}),char(names{i2,3}),datestr(r_time,29),domains);
    n1(i,:)=[names{i1,i3},names{i2,3},t_cell,num2cell(Sallaries2(i)),{Employees_position2(i)},{email},num2cell(numbers(i))];
end

conn = database('#connection_name','#user_name','#password');
sqlwrite(conn,"employees",n1);
close(conn)
clear conn query

function mail=make_an_email(name, surname, date_t, domains)
    mail="";
    r=rand;
    if (r>0.8) && (length(name)>=3)
        mail=mail+char(extractBetween(name,1,3));
    elseif r>0.2
        mail=mail+name;
    else
        mail=mail+char(extractBetween(name,1,1));
    end

    r2=rand;
    if (r2>0.5) 
        mail=mail+".";
    end

    r3=rand;
    if (r3>0.8) && (length(surname)>=3)
        mail=mail+char(extractBetween(surname,1,3));
    elseif (r<=0.2)
        mail=mail+surname;
    elseif (r3>0.2)
        mail=mail+surname;
    else
        mail=mail+char(extractBetween(surname,1,1));
    end

    r4=rand;
    if (strlength(mail)<8)
        mail=mail+char(extractBetween(date_t,1,4));
    elseif r4>0.9
        mail=mail+char(extractBetween(date_t,1,4));
    elseif r4>0.8
        r5=randi([10,9999],1,1);
        mail=mail+int2str(r5);
    elseif r4>0.65
        mail=mail+char(extractBetween(date_t,3,4));
    elseif r4>0.45
        mail=mail+char(extractBetween(date_t,6,7))+char(extractBetween(date_t,9,10));
    elseif r4>0.3
        mail=mail+char(extractBetween(date_t,3,4));
    end    

    r5=randi([1,5],1,1);
    mail=mail+domains(r5);
end
