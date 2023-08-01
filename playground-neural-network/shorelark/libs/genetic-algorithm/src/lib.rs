use rand::Rng;
use rand::RngCore;
use rand::seq::SliceRandom;
use std::ops::Index;

pub fn add(left: usize, right: usize) -> usize {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}

pub struct GeneticAlgorithm<S> {
    selection_method: S,
    crossover_method: Box<dyn CrossoverMethod>,
    mutation_method: Box<dyn MutationMethod>,
}

impl<S> GeneticAlgorithm<S>
    where
        S: SelectionMethod,
        crossover_method: impl CrossoverMethod + 'static,
        mutation_method: impl MutationMethod + 'static, {
    
    pub fn new(selection_method: S) -> Self {
        Self { selection_method,
            crossover_method: Box::new(crossover_method), 
            mutation_method: Box::new(mutation_method),}
    }

    pub fn evolve<I>(
        &self,
        rng: &mut dyn RngCore,
        population: &[I],) -> Vec<I>
        where
            I: Individual, {
        assert!(!population.is_empty());
        (0..population.len())
            .map(|_| {
                let parent_a = self.selection_method.select(rng, population);
                let parent_b = self.selection_method.select(rng, population);

                let mut child = self
                    .crossover_method
                    .crossover(rng, parent_a, parent_b);

                self.mutation_method.mutate(rng, &mut child);

                I::create(child)
                
            })
            .collect()
    }
}

pub trait Individual {
    fn fitness(&self) -> f32;
    fn chromosome(&self) -> &Chromosome;
    fn create(chromosome: Chromosome) -> Self;
}

pub trait SelectionMethod {
    fn select<'a, I>(&self, rng: &mut dyn RngCore, population: &'a[I]) -> &'a I
        where I: Individual;
} 

pub struct RouletteWheelSelection;

impl RouletteWheelSelection {
    pub fn new() -> Self {
        Self
    }
}

impl SelectionMethod for RouletteWheelSelection {
    fn select<'a, I>(&self, rng: &mut dyn RngCore, population: &'a[I]) -> &'a I
            where I: Individual {
        population
                .choose_weighted(rng, |individual| individual.fitness())
                .expect("population is empty")
    }
}

#[derive(Clone, Debug)]
pub struct Chromosome {
    genes: Vec<f32>,
}

impl Chromosome {
    pub fn len(&self) ->usize {
        self.genes.len()
    }
    pub fn iter(&self) -> impl Iterator<Item = &f32> {
        self.genes.iter()
    }
    pub fn iter_mut(&mut self) -> impl Iterator<Item = &mut f32> {
        self.genes.iter_mut()
    }
}

impl Index<usize> for Chromosome {
    type Output = f32;

    fn index(&self, index: usize) -> &Self::Output {
        &self.genes[index]
    }
}

impl FromIterator<f32> for Chromosome {
    fn from_iter<T: IntoIterator<Item = f32>>(iter: T) -> Self {
        Self {
            genes: iter.into_iter().collect(),
        }
    }
}

impl IntoIterator for Chromosome {
    type Item = f32;
    type IntoIter = std::vec::IntoIter<f32>;

    fn into_iter(self) -> Self::IntoIter {
        self.genes.into_iter()
    }
}

pub trait CrossoverMethod {
    fn crossover(
        &self,
        rng: &mut dyn RngCore,
        parent_a: &Chromosome,
        parent_b: &Chromosome,
    ) -> Chromosome;
}

#[derive(Clone, Debug)]
pub struct UniformCrossover;

impl UniformCrossover{
    pub fn new() -> Self {
        Self
    }
}

impl CrossoverMethod for UniformCrossover {
    fn crossover(
        &self,
        rng: &mut dyn RngCore,
        parent_a: &Chromosome,
        parent_b: &Chromosome,
    ) -> Chromosome {
        assert_eq!(parent_a.len(), parent_b.len());
        
        let parent_a = parent_a.iter();
        let parent_b = parent_b.iter();

        parent_a
            .zip(parent_b)
            .map(|(&a, &b)| if rng.gen_bool(0.5) { a } else { b })
            .collect()
        }
    }

    pub trait MutationMethod {
        fn mutate(&self, rng: &mut dyn RngCore, child: &mut Chromosome);
    }

    pub struct GaussianMutation {
        chance: f32,
        coeff: f32,
    }

    impl GaussianMutation {
        pub fn new(chance: f32, coeff: f32) -> Self {
            assert!(chance >= 0.0 && chance <= 1.0);
    
            Self { chance, coeff }
        }
    }
    
    impl MutationMethod for GaussianMutation {
        fn mutate(&self, rng: &mut dyn RngCore, child: &mut Chromosome) {
            for gene in child.iter_mut() {
                let sign = if rng.gen_bool(0.5) { -1.0 } else { 1.0 };
    
                if rng.gen_bool(self.chance as _) {
                    *gene += sign * self.coeff * rng.gen::<f32>();
                }
            }
        }
    }

#[cfg(test)]
impl Individual for TestIndividual {
    fn create(chromosome: Chromosome) -> Self {
        Self::WithChromosome { chromosome }
    }

    fn chromosome(&self) -> &Chromosome {
        match self {
            Self::WithChromosome { chromosome } => chromosome,
            Self::WithFitness { .. } => panic!("not supported for TestIndividual::WithFitness"),
        }
    }

    fn fitness(&self) -> f32 {
        match self {
            Self::WithChromosome { chromosome } => chromosome.iter().sum(),
            Self::WithFitness { fitness } => *fitness,
        }
    }
}