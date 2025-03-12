clc; clear; close all;

% Create the forest terrain (large for full-screen effect)
x = linspace(0, 200, 200);
y = linspace(0, 200, 200);
[X, Y] = meshgrid(x, y);
Z = 15 * peaks(200);  % More realistic height variation

fig = figure('Name', 'Forest Simulation - All Threats', 'NumberTitle', 'off');
ax = axes;
surf(X, Y, Z, 'EdgeColor', 'none');
colormap(summer);  % Greenish terrain
hold on;

% Enable interactivity
rotate3d on;
zoom on;
ax.Clipping = 'off';
ax.Projection = 'perspective';

% Add trees
num_trees = 100;
tree_positions = rand(num_trees, 2) * 200;
for i = 1:num_trees
    tree_x = tree_positions(i, 1);
    tree_y = tree_positions(i, 2);
    tree_z = interp2(X, Y, Z, tree_x, tree_y);
    [cx, cy, cz] = cylinder([0 0.5], 10);
    cz = cz * 5;
    surf(cx + tree_x, cy + tree_y, cz + tree_z, 'FaceColor', [0 0.5 0], 'EdgeColor', 'none');
end

% Initialize threats (time-staged effects)
time_steps = 400; % 40 seconds at 10 FPS
threats = {'Fire', 'Flood', 'Drought', 'Pest', 'Storm', 'Lightning', 'Earthquake', ...
           'Landslide', 'Disease', 'Poaching', 'Deforestation', 'Overgrazing', 'Pollution'};
threat_timings = linspace(1, time_steps, 13); % Spread across 40 sec

% Animation loop
for t = 1:time_steps
    % Clear previous threats (except terrain and trees)
    cla;
    surf(X, Y, Z, 'EdgeColor', 'none');
    colormap(summer);
    hold on;
    
    for i = 1:num_trees
        tree_x = tree_positions(i, 1);
        tree_y = tree_positions(i, 2);
        tree_z = interp2(X, Y, Z, tree_x, tree_y);
        [cx, cy, cz] = cylinder([0 0.5], 10);
        cz = cz * 5;
        surf(cx + tree_x, cy + tree_y, cz + tree_z, 'FaceColor', [0 0.5 0], 'EdgeColor', 'none');
    end
    
    % Activate threats in sequence
    for j = 1:length(threats)
        if t >= threat_timings(j)
            switch threats{j}
                case 'Fire'
                    fire_x = rand * 200;
                    fire_y = rand * 200;
                    fire_z = interp2(X, Y, Z, fire_x, fire_y);
                    [fx, fy, fz] = cylinder([0 3], 10);
                    fz = fz * 8;
                    surf(fx + fire_x, fy + fire_y, fz + fire_z, 'FaceColor', 'r', 'EdgeColor', 'none');
                case 'Flood'
                    fill3([-50 250 250 -50], [-50 -50 250 250], [0 0 0 0], 'b', 'FaceAlpha', 0.3);
                case 'Drought'
                    drought_x = rand * 200;
                    drought_y = rand * 200;
                    fill3(drought_x + [-10 10 10 -10], drought_y + [-10 -10 10 10], [0 0 0 0], 'y');
                case 'Pest'
                    scatter3(rand(1, 50) * 200, rand(1, 50) * 200, ones(1, 50) * 10, 'x', 'MarkerEdgeColor', 'k');
                case 'Storm'
                    fill3([-50 250 250 -50], [-50 -50 250 250], [80 80 80 80], 'c', 'FaceAlpha', 0.3);
                case 'Lightning'
                    line([rand*200, rand*200], [rand*200, rand*200], [80, 0], 'Color', 'y', 'LineWidth', 3);
                case 'Earthquake'
                    plot3([10 190], [100 100], [-2 -2], 'k', 'LineWidth', 5);
                case 'Landslide'
                    fill3([50 70 60], [80 100 90], [30 10 20], [0.5 0.3 0.1]);
                case 'Disease'
                    scatter3(tree_positions(:,1), tree_positions(:,2), ones(num_trees, 1) * 5, 'o', 'MarkerEdgeColor', 'm');
                case 'Poaching'
                    plot3(rand(1, 5) * 200, rand(1, 5) * 200, ones(1, 5) * 5, 'o', 'MarkerEdgeColor', 'r');
                case 'Deforestation'
                    tree_positions = tree_positions(1:end-5, :);
                case 'Overgrazing'
                    fill3([50 70 70 50], [150 150 170 170], [0 0 0 0], [0.5 0.3 0.1]);
                case 'Pollution'
                    fill3([10 30 30 10], [10 10 30 30], [40 50 50 40], 'k', 'FaceAlpha', 0.5);
            end
        end
    end
    
    pause(0.1);
end

disp('Final forest simulation complete!');
