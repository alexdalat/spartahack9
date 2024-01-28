%% Bicycle Model For Real 
%% Goal of Bicycle Model 
% Model the yaw moment of the robot when turning to understand and optimize turning radius and speeds 
%% Initialize Data for Robot 
clear all
close all
clc



Rlength = 0.212; % Length in m from CAD (Estimate)(very tail to very tip) 
Rwidth = 0.146;
Vinit = 0.2; % m/s % Initial Velocity of the Robot 
RMass = 0.59; % Mass of the robot (Estimate)
g = 9.81; % Acceleration due to Gravity 

% Find Torques to Find Yaw Moment 
% Motor data sheet suggests minimum torque 0.15 Nm to 0.6 Nm max torque
% Lateral Acceleration x (G) , yaw moment (Nm) (y) constant velocity (?) 

% Assume right wheel will always be max torque

wheelradius = 0.0348; % Wheel Radius from CAD 
cradius = linspace(0.1,0.7,12); % Corner Radius (Not sure if needed) 
rradius = Rwidth / 2; % Radius for moment assuming Cg is in the middle of the robot 

% Wheel Speed Info 
omegaRi = 200; % RPM Right wheel initial (Constant) 
omegaRrads = (omegaRi * 2*pi) / 60;
omegaLi = 90; % RPM Left wheel initial (Constant) 
omegaLfrads = (omegaLi * 2*pi) / 60;

% Calculate Deceleration of Left wheel for different amounts of rotations 
omegaLf = 90; % RPM Left wheel final 
theta = linspace(0.1,0.5,8); % (Radians)
alphaL = ((omegaLf^0.5) - (omegaLi^0.5)) / 2.*theta;


%% User Selection 
% Prompt User for Selection 

disp('Choose an option:');
disp('1. Wheel Distance Calculations');
disp('2. Plot Position over time');
disp('3. Find Turning Radius ');
disp('4. Plot Turning Angle')

choice = input('Enter the number of your choice: ');

switch choice 
  case 1
%% Wheel Distance Calculations 
% Calculate Different Distance Traveled for wheel
    
t = linspace(0.0,1.5,15);
RDistance = (omegaRrads .* t)*wheelradius;

disp(RDistance);
LDistance = (omegaLfrads .* t)*wheelradius; 
disp(LDistance);
differenced = RDistance - LDistance; 



plot(t, RDistance, 'k', 'linewidth', 2, 'DisplayName', 'Right Wheel')
hold on
plot(t, LDistance, 'r', 'linewidth', 2, 'DisplayName', 'Left Wheel')
plot(t, differenced, 'b', 'linewidth', 2, 'DisplayName', 'differenced')
xlabel("Time (s)")
ylabel("Distance Covered (m)")
title("Distance covered by Left and Right Wheel")
legend('show')
hold off

disp("The difference in position is: (m)")
disp(differenced)

% Plot Position over time 
    case 2
t = linspace(0.0,1.5,15);
RDistance = (omegaRrads .* t)*wheelradius;

disp(RDistance);
LDistance = (omegaLfrads .* t)*wheelradius; 
disp(LDistance);
differenced = RDistance - LDistance; 
Rposition = cumsum(RDistance);
Lposition = cumsum(LDistance);
difference = Rposition - Lposition; 

plot(t , Rposition, 'k' , 'linewidth' , 2, 'DisplayName', 'Right Wheel')
hold on 
plot(t , Lposition, 'r' , 'linewidth' , 2, 'DisplayName', 'Left Wheel')
xlabel("Time (s)")
ylabel("Position (m)")
plot(t, difference, 'b', 'LineWidth', 2, 'DisplayName', 'Position Difference')
title("Position of Right and Left Wheel")
legend('show')
hold off 

%% Find radius 
% Find Radius
    case 3
t = linspace(0.0,1.5,15);
RDistance = (omegaRrads .* t)*wheelradius;

disp(RDistance);
LDistance = (omegaLfrads .* t)*wheelradius; 
disp(LDistance);
differenced = RDistance - LDistance; 
R = LDistance * 0.5; 
% Find angle 
angle = R / RDistance - LDistance;
disp("The turning angle is: ")
disp(angle);
% Plot Turning Radius and Angle 
plot(t,R, 'k','LineWidth', 2, 'DisplayName','Turning Radius')
xlabel("Time (s)")
ylabel("Turning Radius (m)")
title("Turning Radius and Turning Angle Over Time")
% Plot Angle 
    case 4 
t = linspace(0.0,1.5,15);
RDistance = (omegaRrads .* t)*wheelradius;
disp(RDistance);
LDistance = (omegaLfrads .* t)*wheelradius; 
disp(LDistance);
differenced = RDistance - LDistance; 
R = LDistance * 0.5; 
angle = R / RDistance - LDistance;
disp("The turning angle is: ")
disp(angle);
plot(t,angle, 'b','LineWidth', 2, 'DisplayName','Angle')
xlabel("Time(s)")
ylabel("Angle (radians)")
title("Turning Angle Over Time")

    otherwise
        disp("Please choose a valid function (1-4)! ")
end 

