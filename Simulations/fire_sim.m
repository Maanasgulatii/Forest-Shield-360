% fire_simulation.m
clc; clear; close all;

% Step 1: Create the forest terrain (same as before)
x = linspace(0, 100, 100);
y = linspace(0, 100, 100);
[X, Y] = meshgrid(x, y);
Z = 10 * peaks(100);

% Create figure with interactive controls enabled
figure('Name', 'Fire Simulation');
surf(X, Y, Z, 'EdgeColor', 'none');
colormap(summer);
hold on;

% Add trees
num_trees = 50;
tree_positions = rand(num_trees, 2) * 100;

for i = 1:num_trees
    tree_x = tree_positions(i, 1);
    tree_y = tree_positions(i, 2);
    tree_z = interp2(X, Y, Z, tree_x, tree_y);
    [cx, cy, cz] = cylinder([0 0.5], 10);
    cz = cz * 5;
    surf(cx + tree_x, cy + tree_y, cz + tree_z, 'FaceColor', [0 0.5 0], 'EdgeColor', 'none');
end

% Step 2: Initialize fire positions
num_fires = 5; % Number of initial fire spots
fire_positions = rand(num_fires, 2) * 100; % Random fire positions
fire_radius = 2; % Initial fire radius

% Make the simulation interactive with rotation, zoom, and pan
axis vis3d;
rotate3d on;

% Step 3: Animate fire spread
for t = 1:100 % 100 time steps to make the simulation 10 seconds long
    % Plot fire
    for i = 1:num_fires
        fire_x = fire_positions(i, 1);
        fire_y = fire_positions(i, 2);
        fire_z = interp2(X, Y, Z, fire_x, fire_y);
        [fx, fy, fz] = cylinder([0 fire_radius], 20);
        fz = fz * 2; % Fire height
        surf(fx + fire_x, fy + fire_y, fz + fire_z, 'FaceColor', 'r', 'EdgeColor', 'none');
    end

    % Update fire radius to simulate spread
    fire_radius = fire_radius + 0.5;

    % Pause for animation effect (adjust for real-time feel)
    pause(0.1);
end

hold off;
