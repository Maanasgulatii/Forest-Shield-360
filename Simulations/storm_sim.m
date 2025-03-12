% storm_simulation.m
clc; clear; close all;

% Step 1: Create the forest terrain
x = linspace(0, 100, 100);
y = linspace(0, 100, 100);
[X, Y] = meshgrid(x, y);
Z = 10 * peaks(100);  % Creating a terrain with peaks

% Step 2: Create a new figure for storm simulation with full-screen and interactivity
figure('Name', 'Storm Simulation', 'NumberTitle', 'off', 'Position', [0 0 1920 1080]);
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

% Step 3: Simulate storm effects
storm_intensity = 0;  % Initial storm intensity
max_storm_intensity = 10;  % Maximum storm intensity

% Step 4: Enable interactive features
set(gcf, 'WindowButtonDownFcn', @(src, event) disp('Interaction Mode: Click and drag to rotate, scroll to zoom.'));

% Step 5: Animate storm (10-second duration)
for t = 1:100  % 100 time steps for 10 seconds
    % Clear previous frame
    clf;
    
    % Plot terrain and trees again
    surf(X, Y, Z, 'EdgeColor', 'none');
    colormap(summer);  % Terrain color
    hold on;
    
    % Re-plot trees and apply storm effects (swaying)
    for i = 1:num_trees
        tree_x = tree_positions(i, 1);
        tree_y = tree_positions(i, 2);
        tree_z = interp2(X, Y, Z, tree_x, tree_y);
        [cx, cy, cz] = cylinder([0 0.5], 10);
        cz = cz * 5;  % Tree height
        
        % Apply wind effects (trees swaying)
        sway = 0.5 * storm_intensity * sin(t / 5 + i);  % Sinusoidal sway effect
        surf(cx + tree_x + sway, cy + tree_y + sway, cz + tree_z, 'FaceColor', [0 0.5 0], 'EdgeColor', 'none');
    end
    
    % Simulate dark clouds forming
    cloud_density = storm_intensity / max_storm_intensity;  % Cloud density increases with storm intensity
    [cloud_x, cloud_y] = meshgrid(0:1:100, 0:1:100);
    cloud_z = ones(size(cloud_x)) * 20;  % Set cloud height
    cloud_color = [0.5 0.5 0.5] * (1 - cloud_density);  % Darker clouds with more intensity
    
    % Plot storm clouds
    surf(cloud_x, cloud_y, cloud_z, 'FaceColor', cloud_color, 'EdgeColor', 'none');
    
    % Simulate rain
    rain_drops = rand(500, 2) * 100;  % Random raindrop positions
    for i = 1:size(rain_drops, 1)
        rain_x = rain_drops(i, 1);
        rain_y = rain_drops(i, 2);
        rain_z = interp2(X, Y, Z, rain_x, rain_y) + 0.5;  % Raindrops above the ground
        plot3(rain_x, rain_y, rain_z, 'b.', 'MarkerSize', 5);
    end
    
    % Simulate lightning strikes (random flashes)
    if mod(t, 20) == 0  % Lightning every 20 steps
        lightning_x = rand(1) * 100;
        lightning_y = rand(1) * 100;
        lightning_z = interp2(X, Y, Z, lightning_x, lightning_y);
        
        plot3([lightning_x lightning_x], [lightning_y lightning_y], [lightning_z lightning_z + 20], 'y-', 'LineWidth', 3);  % Lightning flash
    end
    
    % Increase storm intensity over time
    storm_intensity = min(storm_intensity + 0.1, max_storm_intensity);
    
    % Pause for animation effect (real-time update)
    pause(0.1);
end

% Enable full 3D view, rotation, and zoom in/out
view(3); % 3D view
axis tight; % Tighten axis limits
rotate3d on; % Enable interactive rotation
zoom on; % Enable zoom in/out
hold off;
