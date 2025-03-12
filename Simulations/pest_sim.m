% pest_disease_simulation.m
clc; clear; close all;

% Step 1: Create the forest terrain
x = linspace(0, 100, 100);
y = linspace(0, 100, 100);
[X, Y] = meshgrid(x, y);
Z = 10 * peaks(100);  % Creating a terrain with peaks

% Step 2: Create a new figure and title it as "Pest/Disease"
figure('Name', 'Pest/Disease Simulation', 'NumberTitle', 'off');
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

% Step 3: Simulate pest/disease spread on trees
num_pests = 30;  % More visible pests
pest_positions = rand(num_pests, 2) * 100;  % Random pest positions

% Step 4: Animate pest/disease spread (10-second duration)
for t = 1:100  % 100 time steps for 10 seconds
    % Clear previous frame
    clf;
    
    % Plot terrain and trees again
    surf(X, Y, Z, 'EdgeColor', 'none');
    colormap(summer);  % Terrain color
    hold on;
    
    % Re-plot trees, and show pest/disease effects on them
    for i = 1:num_trees
        tree_x = tree_positions(i, 1);
        tree_y = tree_positions(i, 2);
        tree_z = interp2(X, Y, Z, tree_x, tree_y);
        [cx, cy, cz] = cylinder([0 0.5], 10);
        cz = cz * 5;  % Tree height
        % Apply pest/disease effect by changing the tree color to brown/decayed
        if any(vecnorm(pest_positions - [tree_x tree_y], 2, 2) < 5)  % Trees near pests
            surf(cx + tree_x, cy + tree_y, cz + tree_z, 'FaceColor', [0.5 0.2 0], 'EdgeColor', 'none');
        else
            surf(cx + tree_x, cy + tree_y, cz + tree_z, 'FaceColor', [0 0.5 0], 'EdgeColor', 'none');
        end
    end
    
    % Spread pests (random movement in the forest)
    pest_positions = pest_positions + rand(num_pests, 2) * 2 - 1;  % Random movement of pests
    
    % Show pest marks on the ground (visual effect)
    for i = 1:num_pests
        pest_x = pest_positions(i, 1);
        pest_y = pest_positions(i, 2);
        scatter3(pest_x, pest_y, 0, 100, [0.5 0.1 0], 'filled');  % Larger pests visible on ground
    end

    % Enable interactivity (rotation and zoom)
    rotate3d on;
    axis([0 100 0 100 -10 20]);  % Keep axis fixed for better view
    
    % Pause to create animation effect (real-time update)
    pause(0.1);
end

hold off;
