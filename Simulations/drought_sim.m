% drought_simulation.m
clc; clear; close all;

% Step 1: Create the forest terrain
x = linspace(0, 100, 100);
y = linspace(0, 100, 100);
[X, Y] = meshgrid(x, y);
Z = 10 * peaks(100);  % Creating a terrain with peaks

% Step 2: Create a new figure and title it as "Drought"
figure('Name', 'Drought Simulation', 'NumberTitle', 'off'); 
surf(X, Y, Z, 'EdgeColor', 'none');
colormap(summer);  % Set terrain color (greenish for forest)
hold on;

% Add trees (cylinders)
num_trees = 50;
tree_positions = rand(num_trees, 2) * 100;  % Random tree positions

for i = 1:num_trees
    tree_x = tree_positions(i, 1);
    tree_y = tree_positions(i, 2);
    tree_z = interp2(X, Y, Z, tree_x, tree_y);
    [cx, cy, cz] = cylinder([0 0.5], 10);
    cz = cz * 5;  % Tree height
    surf(cx + tree_x, cy + tree_y, cz + tree_z, 'FaceColor', [0 0.5 0], 'EdgeColor', 'none');
end

% Step 3: Initialize drought (reduce vegetation over time)
drought_level = 0;  % Initial drought level

% Step 4: Animate the drought (10-second duration)
for t = 1:100  % 100 time steps for 10 seconds
    % Clear previous frame
    clf;
    
    % Plot terrain and trees again
    surf(X, Y, Z, 'EdgeColor', 'none');
    colormap(summer);  % Terrain color
    hold on;
    
    % Re-plot trees with reduced size over time to simulate drought
    for i = 1:num_trees
        tree_x = tree_positions(i, 1);
        tree_y = tree_positions(i, 2);
        tree_z = interp2(X, Y, Z, tree_x, tree_y);
        [cx, cy, cz] = cylinder([0 0.5 - drought_level], 10);  % Decrease tree height over time
        cz = cz * 5;
        surf(cx + tree_x, cy + tree_y, cz + tree_z, 'FaceColor', [0 0.5 0], 'EdgeColor', 'none');
    end
    
    % Increase drought level to simulate drying out vegetation
    drought_level = drought_level + 0.01;

    % Enable interactivity (rotation and zoom)
    rotate3d on;
    axis([0 100 0 100 -10 20]);  % Keep axis fixed for better view
    
    % Pause to create animation effect (real-time update)
    pause(0.1);
end

hold off;
